from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with extra fields if needed"""

    pass


class Employee(models.Model):
    """Employee model linked to the User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
