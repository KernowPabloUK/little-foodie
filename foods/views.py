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
    Render the main food page for authenticated users.

    Returns:
        HttpResponse: The rendered 'foods/food.html' template.
    """
    return render(request, 'foods/food.html')


@require_http_methods(["GET"])
def food_details_api(request, food_id):
    """
    API endpoint to retrieve details about a specific food item.

    Returns a JSON response containing food details such as name, category,
    minimum age, allergen status, image path, favourite status for the
    selected child, and authorisation status. If the user is authenticated
    and a selected child is set in the session, checks if there is a recent
    favourite log for this food and child.

    Args:
        request (HttpRequest): The HTTP request object.
        food_id (int): The primary key of the food item to retrieve.

    Returns:
        JsonResponse: A JSON object with food details.
    """
    food = get_object_or_404(Food, pk=food_id)

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

    return JsonResponse({
        'id': food.id,
        'name': food.name,
        'category': food.get_category_display(),
        'min_age_months': food.min_age_months,
        'is_allergen': food.is_allergen,
        'image': static(food.image) if food.image else None,
        'is_favourite': is_favourite,
        'is_authorised': food.is_authorised,
    })
