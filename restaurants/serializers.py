from django.utils import timezone
from rest_framework import serializers

from .models import Menu, MenuItem, Restaurant


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price"]


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    restaurant_name = serializers.ReadOnlyField(source="restaurant.name")

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "restaurant_name", "date", "description", "items"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)
        for item_data in items_data:
            MenuItem.objects.create(menu=menu, **item_data)
        return menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "address", "contact_email", "contact_phone"]
        read_only_fields = ["id"]


class RestaurantDetailSerializer(RestaurantSerializer):
    menus = serializers.SerializerMethodField()

    class Meta(RestaurantSerializer.Meta):
        fields = RestaurantSerializer.Meta.fields + ["menus"]

    def get_menus(self, obj):
        # Only return today's menu if it exists
        today = timezone.now().date()
        menu = obj.menus.filter(date=today).first()
        if menu:
            return MenuSerializer(menu).data
        return None
