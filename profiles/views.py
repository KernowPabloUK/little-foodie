from django.shortcuts import render


# Create your views here.
def home_view(request):
    """Home page view - accessible to all users"""
    return render(request, 'profiles/home.html')
