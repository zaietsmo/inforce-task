from django.db import models
from django.utils import timezone

from restaurants.models import Menu
from users.models import Employee


def get_current_date():
    """Return current date for default value"""
    return timezone.now().date()


class Vote(models.Model):
    """Employee votes for a menu"""

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    date = models.DateField(default=get_current_date)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "date")

    def __str__(self):
        return f"{self.employee.user.username} voted for {self.menu.restaurant.name} on {self.date}"
