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
    
    data = {
        'id': food.id,
        'name': food.name,
        'category': food.get_category_display(),
        'min_age_months': food.min_age_months,
        'is_allergen': food.is_allergen,
        'image': food.image.url if food.image else None
    }
    
    return JsonResponse(data)
