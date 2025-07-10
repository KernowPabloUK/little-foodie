from django.db import models
from django.contrib.auth.models import User
from children.models import Child
from foods.models import Food

CONSISTENCY = ((0, "Purée"), (1, "Mashed"), (2, "Finger food"), (3, "Liquid"))
PREPARATION = ((0, "Raw"), (1, "Cooked"))
FEED_METHOD = ((0, "Spoon Fed"), (1, "Self Fed"))
SATISFACTION = ((0, "Dislike"), (1, "Indifferent"), (2, "Like"), (3, "Love"))


# Create your models here.
class Consistency(models.Model):
    """
    Stores a consistency entry related to
    :model:`logs.FoodLog`
    """
    label = models.IntegerField(choices=CONSISTENCY, default=1)

    def __str__(self):
        return self.get_label_display()  # This will return the human-readable choice


class Preparation(models.Model):
    """
    Stores a preperation entry related to
    :model:`logs.FoodLog`
    """
    label = models.IntegerField(choices=PREPARATION, default=1)

    def __str__(self):
        return self.get_label_display()


class FeedingMethod(models.Model):
    """
    Stores a feeding method entry related to
    :model:`logs.FoodLog`
    """
    label = models.IntegerField(choices=FEED_METHOD, default=1)

    def __str__(self):
        return self.get_label_display()


class SatisfactionLevel(models.Model):
    """
    Stores a satisfaction level entry related to
    :model:`logs.FoodLog`
    """
    label = models.IntegerField(choices=SATISFACTION, default=1)

    def __str__(self):
        return self.get_label_display()


class FoodLog(models.Model):
    """
    Stores a food log entry related to
    :model:`auth.User`,
    :model:`children.Child`,
    :model:`foods.Food`,
    :model:`logs.Consistency`,
    :model:`logs.Preparation`,
    :model:`logs.FeedingMethod`
    :model:`logs.SatisfactionLevel`
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="food_logs")
    child = models.ForeignKey(Child, on_delete=models.PROTECT, related_name="food_logs")
    food = models.ForeignKey(Food, on_delete=models.PROTECT, related_name="food_logs")
    consistency = models.ForeignKey(Consistency, on_delete=models.PROTECT, related_name="food_logs")
    preparation = models.ForeignKey(Preparation, on_delete=models.PROTECT, related_name="food_logs")
    feeding_method = models.ForeignKey(FeedingMethod, on_delete=models.PROTECT, related_name="food_logs")
    satisfaction_level = models.ForeignKey(SatisfactionLevel, on_delete=models.PROTECT, related_name="food_logs")
    volume = models.IntegerField(default=0)
    favourite = models.BooleanField(default=False)
    notes = models.CharField(null=True, blank=True, max_length=200)
    logged_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-logged_at"]

    def __str__(self):
        return f"{self.child} has tried {self.food}, this has been logged at {self.logged_at}"
