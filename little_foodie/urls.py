"""
URL configuration for little_foodie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from children.views import my_children
from foods.views import my_foods
from logs.views import my_logs
from stats.views import my_stats
from profiles.views import home_view


def redirect_to_home(request):
    """
    On login, user is redirected to the updated homepage
    """
    return redirect('home')


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', redirect_to_home, name='profile_redirect'),
    path('children/', my_children, name='children'),
    path('foods/', my_foods, name='foods'),
    path('logs/', my_logs, name='logs'),    
    path('stats/', my_stats, name='stats'),
]
