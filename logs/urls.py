from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_log_view, name='logs'),
    path('clear-child/', views.clear_child_selection, name='clear_child_selection'),
    path('edit/<int:log_id>/', views.edit_food_log, name='edit_food_log'),
    path('foods/create/', views.create_food_ajax, name='create_food_ajax'),
    ]
