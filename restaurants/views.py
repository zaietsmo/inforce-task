from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Menu, Restaurant
from .serializers import (
    MenuSerializer,
    RestaurantDetailSerializer,
    RestaurantSerializer,
)

# Create your views here.


class RestaurantViewSet(viewsets.ModelViewSet):
    """API endpoint for restaurants management"""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RestaurantDetailSerializer
        return RestaurantSerializer

    @action(detail=True, methods=["post"])
    def upload_menu(self, request, pk=None):
        """Upload a menu for a specific restaurant"""
        restaurant = self.get_object()

        data = request.data.copy()
        data["restaurant"] = restaurant.pk

        if "date" not in data:
            data["date"] = timezone.now().date()

        # Check if menu already exists for this date
        existing_menu = Menu.objects.filter(
            restaurant=restaurant, date=data["date"]
        ).first()

        serializer = (
            MenuSerializer(existing_menu, data=data)
            if existing_menu
            else MenuSerializer(data=data)
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for menus"""

    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.all()

    @action(detail=False, methods=["get"])
    def today(self, request):
        """Get all menus for today"""
        today = timezone.now().date()
        queryset = Menu.objects.filter(date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
