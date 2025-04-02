from django.db.models import Count
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Vote
from .serializers import VoteResultSerializer, VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """API endpoint for voting"""

    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.all()

    def create(self, request):
        data = request.data.copy()
        data["date"] = timezone.now().date()

        try:
            employee = request.user.employee
            data["employee"] = employee.pk
        except AttributeError:
            return Response(
                {"error": "User has no associated employee profile"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def results(self, request):
        """Get voting results for today"""
        today = timezone.now().date()

        # Count votes for each menu
        results = (
            Vote.objects.filter(date=today)
            .values("menu", "menu__restaurant__name", "menu__description")
            .annotate(vote_count=Count("id"))
            .order_by("-vote_count")
        )

        result_data = []
        for r in results:
            result_data.append(
                {
                    "menu_id": r["menu"],
                    "restaurant_name": r["menu__restaurant__name"],
                    "menu_description": r["menu__description"],
                    "vote_count": r["vote_count"],
                }
            )

        serializer = VoteResultSerializer(result_data, many=True)
        return Response(serializer.data)
