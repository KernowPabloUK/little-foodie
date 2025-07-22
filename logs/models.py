from django.db import models
from django.contrib.auth.models import User
from children.models import Child
from foods.models import Food

CONSISTENCY = ((0, "Purée"), (1, "Mashed"), (2, "Finger food"), (3, "Liquid"))
PREPARATION = ((0, "Raw"), (1, "Cooked"))
FEED_METHOD = ((0, "Spoon Fed"), (1, "Self Fed"))
SATISFACTION = ((0, "Dislike"), (1, "Indifferent"), (2, "Like"), (3, "Love"))


class Consistency(models.Model):
    """
    Model representing the consistency of a food log entry.

    Used to specify how the food was prepared in terms of texture
    (e.g., purée, mashed).
    Related to :model:`logs.FoodLog`.
    """
    label = models.IntegerField(choices=CONSISTENCY, default=1)

    def __str__(self):
        """
        Return the display value of the consistency label.
        """
        return self.get_label_display()


class Preparation(models.Model):
    """
    Model representing the preparation method of a food log entry.

    Used to specify whether the food was raw or cooked.
    Related to :model:`logs.FoodLog`.
    """
    label = models.IntegerField(choices=PREPARATION, default=1)

    def __str__(self):
        """
        Return the display value of the preparation label.
        """
        return self.get_label_display()


class FeedingMethod(models.Model):
    """
    Model representing the feeding method of a food log entry.

    Used to specify how the food was fed (e.g., spoon fed, self fed).
    Related to :model:`logs.FoodLog`.
    """
    label = models.IntegerField(choices=FEED_METHOD, default=1)

    def __str__(self):
        """
        Return the display value of the feeding method label.
        """
        return self.get_label_display()


class SatisfactionLevel(models.Model):
    """
    Model representing the satisfaction level of a food log entry.

    Used to specify the child's reaction to the food
    (e.g., dislike, like, love).
    Related to :model:`logs.FoodLog`.
    """
    label = models.IntegerField(choices=SATISFACTION, default=1)

    def __str__(self):
        """
        Return the display value of the satisfaction level label.
        """
        return self.get_label_display()


class FoodLog(models.Model):
    """
    Model representing a food log entry.

    Stores information about a feeding event, including the user, child, food,
    consistency, preparation, feeding method, satisfaction level, volume,
    favourite status, notes, and the date/time the log was created.

    Related to:
        :model:`auth.User`
        :model:`children.Child`
        :model:`foods.Food`
        :model:`logs.Consistency`
        :model:`logs.Preparation`
        :model:`logs.FeedingMethod`
        :model:`logs.SatisfactionLevel`
    """
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    child = models.ForeignKey(
        Child,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name="food_logs",
        null=False,
        blank=False
    )
    consistency = models.ForeignKey(
        Consistency,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    preparation = models.ForeignKey(
        Preparation,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    feeding_method = models.ForeignKey(
        FeedingMethod,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    satisfaction_level = models.ForeignKey(
        SatisfactionLevel,
        on_delete=models.PROTECT,
        related_name="food_logs",
        null=False,
        blank=False
    )
    volume = models.IntegerField(null=False, blank=False)
    favourite = models.BooleanField(default=False, null=False, blank=False)
    notes = models.CharField(null=True, blank=True, max_length=200)
    logged_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for FoodLog model.

        Orders food logs by most recent first.
        """
        ordering = ["-logged_at"]

    def __str__(self):
        """
        Return a string representation of the food log entry.
        """
        return (
            f"{self.child} has tried {self.food}, "
            f"this has been logged at {self.logged_at}"
        )
