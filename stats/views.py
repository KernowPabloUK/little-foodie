from django.shortcuts import render, redirect
from children.models import Child
from logs.models import FoodLog
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from profiles.models import Profile
from foods.models import FOOD_CATEGORY


# Create your views here.

@login_required
def statistics_view(request):
    """
    Display statistics for a user's children and their food logs.

    This view gathers and aggregates food log data for the selected child,
    including counts, volumes, and average satisfaction for each food and
    food category. It prepares the data for charting and visualization
    in the statistics template. If no child is selected, defaults to the
    first child in the user's profile.

    Returns:
        HttpResponse: The rendered 'stats/statistics.html' template with
        statistics context for the selected child.
    """
    profile = Profile.objects.get(user=request.user)
    children = Child.objects.filter(user=profile)
    if not children.exists():
        return redirect('add_child')

    selected_child_id = request.GET.get('child_id')
    if not selected_child_id and children.exists():
        selected_child_id = children.first().id
    food_logs = (
        FoodLog.objects.filter(child_id=selected_child_id)
        if selected_child_id else FoodLog.objects.none()
    )
    food_counts = (
        food_logs.values('food__name', 'food__image')
        .annotate(
            count=Count('id'),
            total_volume=Sum('volume'),
            avg_satisfaction=Avg('satisfaction_level__label')
        )
        .order_by('-count')
    )
    food_stats = {
        'labels': [
            {
                'name': f['food__name'],
                'image': f['food__image'],
                'satisfaction': int(round(f['avg_satisfaction'] or 0))
            }
            for f in food_counts
        ],
        'counts': [f['count'] for f in food_counts],
        'volumes': [f['total_volume'] or 0 for f in food_counts],
    }
    satisfaction_range = [0, 1, 2, 3]

    # Category stats
    category_counts = (
        food_logs.values('food__category')
        .annotate(
            count=Count('id'),
            total_volume=Sum('volume'),
            avg_satisfaction=Avg('satisfaction_level__label')
        )
        .order_by('-count')
    )
    CATEGORY_MAP = dict(FOOD_CATEGORY)
    category_image_map = {
        'Fruit': 'images/category_images/fruit.png',
        'Vegetable': 'images/category_images/vegetable.png',
        'Starch': 'images/category_images/starch.png',
        'Dairy': 'images/category_images/dairy.png',
        'Protein': 'images/category_images/protein.png',
    }
    category_stats = {
        'labels': [
            {
                'name': CATEGORY_MAP.get(c['food__category'], 'Unknown'),
                'image': category_image_map.get(
                    CATEGORY_MAP.get(
                        c['food__category'],
                        'Unknown'
                    ),
                    ''
                ),
                'satisfaction': int(round(c['avg_satisfaction'] or 0))
            }
            for c in category_counts
        ],
        'counts': [c['count'] for c in category_counts],
        'volumes': [c['total_volume'] or 0 for c in category_counts],
    }

    selected_child = (
        children.get(id=selected_child_id)
        if selected_child_id else None
    )

    return render(request, 'stats/statistics.html', {
        'children': children,
        'selected_child_id': (
            int(selected_child_id) if selected_child_id else None
        ),
        'selected_child': selected_child,
        'food_stats': food_stats,
        'category_stats': category_stats,
        'satisfaction_range': satisfaction_range,
    })
