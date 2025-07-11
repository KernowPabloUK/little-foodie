from django.db import models
from datetime import date
from profiles.models import Profile
from django.core.exceptions import ValidationError


def validate_birthdate(value):
    """Validate that birthdate is not in the future"""
    if value > date.today():
        raise ValidationError('Birth date cannot be in the future.')


# Create your models here.
class Child(models.Model):
    """
    Stores a Child entry related to
    :model:`auth.User`
    :model:`logs.FoodLog`
    """
    user = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="children"
    )
    name = models.CharField(max_length=30)
    birthdate = models.DateField(validators=[validate_birthdate])

    class Meta:
        ordering = ["-birthdate"]
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name}"

    @property
    def age_in_months(self):
        today = date.today()
        years = today.year - self.birthdate.year
        months = today.month - self.birthdate.month
        days = today.day - self.birthdate.day
        total_months = years * 12 + months
        if days < 0:
            total_months -= 1
        return total_months
