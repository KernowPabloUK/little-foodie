from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_child, name='add_child'),
    path('delete/<int:child_id>/', views.confirm_delete_child, name='confirm_delete_child'),
]
