from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_log_view, name='logs'),
    ]
