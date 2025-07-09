from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_view(request):
    """
    Home page view - accessible to all users
    """
    return render(request, 'profiles/home.html')


@login_required
def profile_view(request):
    """
    Loads the profile page - logged in users only
    """
    return render(request, 'profiles/profile.html')
