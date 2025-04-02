import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from restaurants.models import Menu, Restaurant
from users.models import Employee, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username="testuser", password="password")
    Employee.objects.create(user=user, department="IT")
    client = APIClient()
    response = client.post(
        reverse("token_obtain_pair"), {"username": "testuser", "password": "password"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.mark.django_db
def test_create_restaurant(authenticated_client):
    url = reverse("restaurant-list")
    data = {
        "name": "Test Restaurant",
        "address": "123 Test Street",
        "contact_email": "test@example.com",
        "contact_phone": "1234567890",
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Restaurant.objects.count() == 1
    assert Restaurant.objects.get().name == "Test Restaurant"


@pytest.mark.django_db
def test_upload_menu(authenticated_client):
    # Create a restaurant first
    restaurant = Restaurant.objects.create(
        name="Test Restaurant", address="Test Address"
    )

    url = reverse("restaurant-upload-menu", kwargs={"pk": restaurant.pk})
    today = timezone.now().date().isoformat()

    data = {
        "date": today,
        "description": "Daily special menu",
        "items": [
            {
                "name": "Pasta",
                "description": "Delicious pasta with sauce",
                "price": "9.99",
            },
            {"name": "Salad", "description": "Fresh garden salad", "price": "4.99"},
        ],
    }

    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Check that menu was created with items
    assert Menu.objects.count() == 1
    menu = Menu.objects.first()
    assert menu.items.count() == 2
