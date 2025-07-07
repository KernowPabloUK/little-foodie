from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def my_children(request):
    return HttpResponse("CHILDREN")
