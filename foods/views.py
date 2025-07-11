from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.templatetags.static import static
from .models import Food
from logs.models import FoodLog


# Create your views here.
@login_required
def food_view(request):
    """
    TODO
    """
    return render(request, 'foods/food.html')


@require_http_methods(["GET"])
def food_details_api(request, food_id):
    """
    API endpoint to get food details for the food log form
    """
    try:
        food = Food.objects.get(id=food_id)

        is_favourite = False
        if request.user.is_authenticated:
            selected_child_id = request.session.get('selected_child_id')
            if selected_child_id:
                recent_favourite_log = FoodLog.objects.filter(
                    food=food,
                    child_id=selected_child_id,
                    favourite=True
                ).order_by('-logged_at').first()

                if recent_favourite_log:
                    is_favourite = True
                    is_favourite = True

        data = {
            'id': food.id,
            'name': food.name,
            'category': food.get_category_display(),
            'min_age_months': food.min_age_months,
            'is_allergen': food.is_allergen,
            'image': static(food.image) if food.image else None,  # Generates the full static URL
            'is_favourite': is_favourite,
        }

        return JsonResponse(data)
    except Food.DoesNotExist:
        return JsonResponse({'error': 'Food not found'}, status=404)
