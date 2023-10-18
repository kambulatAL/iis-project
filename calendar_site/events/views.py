from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from events.models import *

# Create your views here.
def index(request):
    users = RegisteredUser.objects.all()
    return render(request, "index.html", {"title": "Home", "users": users})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')