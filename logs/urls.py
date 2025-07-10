from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_log_view, name='logs'),
    path('clear-child/', views.clear_child_selection, name='clear_child_selection'),
    ]
