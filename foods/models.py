from django.db import models
from django.contrib.auth.models import User

FOOD_CATEGORY = (
    (0, "Fruit"),
    (1, "Vegetable"),
    (2, "Starch"),
    (3, "Dairy"),
    (4, "Protein")
)


class Food(models.Model):
    """
    Model representing a food item.

    Fields:
        name (CharField): The name of the food (unique).
        category (IntegerField): The food category, chosen from FOOD_CATEGORY.
        min_age_months (IntegerField): Minimum recommended age in months.
        is_allergen (BooleanField): Whether the food is a common allergen.
        image (ImageField): Optional image of the food.
        is_authorised (BooleanField): Whether the food is authorised for use.
        created_by_user (ForeignKey): The user who created this food entry.

    Meta:
        ordering: Foods are ordered by name descending.

    Methods:
        __str__: Returns the food's name as its string representation.
    """
    name = models.CharField(max_length=30, unique=True)
    category = models.IntegerField(choices=FOOD_CATEGORY, default=0)
    min_age_months = models.IntegerField(default=0)
    is_allergen = models.BooleanField(default=False)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    is_authorised = models.BooleanField(default=False)
    created_by_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="foods"
    )

    class Meta:
        """
        Meta options for the Food model.
        Foods are ordered by name in descending order.
        """
        ordering = ["-name"]

    def __str__(self):
        """
        Return the string representation of the food, which is its name.
        """
        return self.name
