from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from events.models import *

#TODO: то, что у нас в фигме Settings - тут называется My profile
# Menu bar
menu = ["Login", "Sign up", "Events", "My events", "My profile", "Logout"]

# Create your views here.
def index(request):
    users = RegisteredUser.objects.all()
    return render(request, "index.html", {"menu": menu, "title": "Home", "users": users})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')