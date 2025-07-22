from django.db import models
from datetime import date
from profiles.models import Profile
from django.core.exceptions import ValidationError


def validate_birthdate(value):
    """
    Validator to ensure the birthdate is not in the future.

    Args:
        value (date): The birthdate to validate.

    Raises:
        ValidationError: If the birthdate is in the future.
    """
    if value > date.today():
        raise ValidationError('Birth date cannot be in the future.')


class Child(models.Model):
    """
    Model representing a child associated with a user profile.

    Fields:
        user (ForeignKey): Reference to the Profile this child belongs to.
        name (CharField): The child's name.
        birthdate (DateField): The child's birthdate,
        validated to not be in the future.

    Meta:
        ordering: Children are ordered by birthdate descending.
        unique_together: Each child name must be unique per user.

    Methods:
        __str__: Returns the child's name as its string representation.
        age_in_months: Calculates the child's age in months.
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
        """
        Return the string representation of the child,
        which is the child's name.
        """
        return f"{self.name}"

    @property
    def age_in_months(self):
        """
        Calculate and return the child's age in months.

        Returns:
            int: The age of the child in months.
        """
        today = date.today()
        years = today.year - self.birthdate.year
        months = today.month - self.birthdate.month
        days = today.day - self.birthdate.day
        total_months = years * 12 + months
        if days < 0:
            total_months -= 1
        return total_months
