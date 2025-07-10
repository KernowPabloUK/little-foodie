from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_view, name='foods'),
    path(
        'api/details/<int:food_id>/',
        views.food_details_api,
        name='food_details_api',
    ),
    ]
