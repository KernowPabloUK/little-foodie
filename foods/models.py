from django.db import models
from django.contrib.auth.models import User

FOOD_CATEGORY = (
    (0, "Fruit"),
    (1, "Vegetable"),
    (2, "Starch"),
    (3, "Dairy"),
    (4, "Protein")
    )


# Create your models here.
class Food(models.Model):
    """
    Stores a food entry related to
    :model:`auth.User`
    :model:`logs.FoodLog`
    """
    name = models.CharField(max_length=30, unique=True)
    category = models.IntegerField(choices=FOOD_CATEGORY, default=0)
    min_age_months = models.IntegerField(default=0)
    is_allergen = models.BooleanField(default=False)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    created_by_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="foods"
    )

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
