from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def food_view(request):
    """
    TODO
    """
    return render(request, 'foods/food.html')
