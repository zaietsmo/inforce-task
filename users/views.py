from rest_framework import permissions, viewsets

from .models import Employee
from .serializers import EmployeeSerializer

# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    """API endpoint for employees management"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            # Allow any for employee creation
            return [permissions.AllowAny()]
        return super().get_permissions()
