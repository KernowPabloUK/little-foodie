from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """
    Model representing a user profile.

    Stores additional information about a user, such as first name, last name,
    and birth date, and is related to the built-in Django User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the profile, showing the username.
        """
        return f"{self.user.username}'s profile"

    class Meta:
        """
        Meta options for the Profile model.
        Orders profiles by creation date, newest first.
        """
        ordering = ['-created_at']
