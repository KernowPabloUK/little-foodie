from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def my_stats(request):
    return HttpResponse("STATS")
