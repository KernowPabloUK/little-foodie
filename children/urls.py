from django.urls import path
from . import views
from profiles import views

urlpatterns = [
    path('add/', views.add_child, name='add_child'),
    ]
