from django.shortcuts import render
from children.models import Child
from logs.models import FoodLog
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from profiles.models import Profile
import math


# Create your views here.
@login_required
def statistics_view(request):
    profile = Profile.objects.get(user=request.user)
    children = Child.objects.filter(user=profile)
    selected_child_id = request.GET.get('child_id')
    if not selected_child_id and children.exists():
        selected_child_id = children.first().id
    food_logs = FoodLog.objects.filter(child_id=selected_child_id) if selected_child_id else FoodLog.objects.none()
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
                'satisfaction': int(round(f['avg_satisfaction'] or 0))
            }
            for f in food_counts
        ],
        'counts': [f['count'] for f in food_counts],
        'volumes': [f['total_volume'] or 0 for f in food_counts],
    }
    satisfaction_range = [0, 1, 2, 3]
    return render(request, 'stats/statistics.html', {
        'children': children,
        'selected_child_id': int(selected_child_id) if selected_child_id else None,
        'food_stats': food_stats,
        'satisfaction_range': satisfaction_range,
    })
