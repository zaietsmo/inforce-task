from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "employee", "menu", "date"]
        read_only_fields = ["id", "date"]

    def validate(self, data):
        # Check if employee already voted today
        employee = data["employee"]
        from django.utils import timezone

        today = timezone.now().date()

        if Vote.objects.filter(employee=employee, date=today).exists():
            raise serializers.ValidationError("You have already voted today")

        return data


class VoteResultSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    restaurant_name = serializers.CharField()
    menu_description = serializers.CharField()
    vote_count = serializers.IntegerField()
