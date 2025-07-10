from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Food


# Create your views here.
@login_required
def food_view(request):
    """
    TODO
    """
    return render(request, 'foods/food.html')


@login_required
def food_details_api(request, food_id):
    """
    API endpoint to get food details for the food log form
    """
    food = get_object_or_404(Food, id=food_id)

    # Handle different category field types
    if hasattr(food, 'category'):
        if hasattr(food.category, 'name'):
            category_display = food.category.name
        elif hasattr(food, 'get_category_display'):
            category_display = food.get_category_display()
        else:
            category_display = str(food.category)
    else:
        category_display = 'Unknown'

    # Get image URL from the database field
    image_url = None
    if hasattr(food, 'image') and food.image:
        image_url = food.image.url

    data = {
        'id': food.id,
        'name': food.name,
        'category': category_display,
        'min_age_months': food.min_age_months if food.min_age_months else 0,
        'is_allergen': food.is_allergen,
        'image': image_url
    }

    return JsonResponse(data)
