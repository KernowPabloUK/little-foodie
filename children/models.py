from django.db import models
from django.contrib.auth.models import User
from datetime import date
from profiles.models import Profile


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
    name = models.CharField(max_length=30, unique=True)
    birthdate = models.DateField()
    # TODO
    # profile_image = models.ImageField()
    # profile_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ["-birthdate"]

    def __str__(self):
        return f"{self.name} has been registered."

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
