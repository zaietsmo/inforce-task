import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from restaurants.models import Menu, Restaurant
from users.models import Employee, User
from votes.models import Vote


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username="testuser", password="password")
    employee = Employee.objects.create(user=user, department="IT")
    client = APIClient()
    response = client.post(
        reverse("token_obtain_pair"), {"username": "testuser", "password": "password"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, employee


@pytest.mark.django_db
def test_cast_vote(authenticated_client):
    client, employee = authenticated_client

    # Create restaurant and menu
    restaurant = Restaurant.objects.create(
        name="Test Restaurant", address="Test Address"
    )
    menu = Menu.objects.create(
        restaurant=restaurant, date=timezone.now().date(), description="Test Menu"
    )

    url = reverse("vote-list")
    data = {"menu": menu.pk}

    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Check that vote was created
    assert Vote.objects.count() == 1
    vote = Vote.objects.first()
    assert vote.menu == menu
    assert vote.employee == employee


@pytest.mark.django_db
def test_vote_results(authenticated_client):
    client, employee = authenticated_client

    # Create restaurants and menus
    restaurant1 = Restaurant.objects.create(name="Restaurant 1", address="Address 1")
    restaurant2 = Restaurant.objects.create(name="Restaurant 2", address="Address 2")

    menu1 = Menu.objects.create(
        restaurant=restaurant1, date=timezone.now().date(), description="Menu 1"
    )
    menu2 = Menu.objects.create(
        restaurant=restaurant2, date=timezone.now().date(), description="Menu 2"
    )

    # Create votes
    Vote.objects.create(employee=employee, menu=menu1, date=timezone.now().date())

    # Create another user and vote
    user2 = User.objects.create_user(username="testuser2", password="password")
    employee2 = Employee.objects.create(user=user2, department="HR")
    Vote.objects.create(employee=employee2, menu=menu1, date=timezone.now().date())

    # Create a third user who votes for menu2
    user3 = User.objects.create_user(username="testuser3", password="password")
    employee3 = Employee.objects.create(user=user3, department="Finance")
    Vote.objects.create(employee=employee3, menu=menu2, date=timezone.now().date())

    # Get results
    url = reverse("vote-results")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    # Check if menu1 has 2 votes and is first
    assert response.data[0]["menu_id"] == menu1.pk
    assert response.data[0]["vote_count"] == 2

    # Check if menu2 has 1 vote and is second
    assert response.data[1]["menu_id"] == menu2.pk
    assert response.data[1]["vote_count"] == 1
