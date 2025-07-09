from django.urls import path
from . import views

urlpatterns = [
    path('', views.child_view, name='children'),
    ]
