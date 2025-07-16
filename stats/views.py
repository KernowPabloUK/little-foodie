from django.shortcuts import render
from children.models import Child
from logs.models import FoodLog
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from profiles.models import Profile


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
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    food_stats = {
        'labels': [f['food__name'] for f in food_counts],
        'counts': [f['count'] for f in food_counts],
    }
    return render(request, 'stats/statistics.html', {
        'children': children,
        'selected_child_id': int(selected_child_id) if selected_child_id else None,
        'food_stats': food_stats,
    })
