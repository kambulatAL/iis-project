from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from events.models import RegisteredUser, EventPlace
from .forms import LoginForm, RegisterForm
from django.contrib import messages


def list_places(request):
    places = EventPlace.objects.all()
    return render(request, "admin_temps/list_places.html", {"title": "List of places", "places": places})

def list_users(request):
    users = RegisteredUser.objects.all()
    return render(request, "admin_temps/list_users.html", {"title": "List of users", "users": users})


############################################################################################### Admin functions

#function that delete user from database by username
def delete_user(request, username):
    # check if user is admin
    if request.user.is_authenticated and request.user.is_admin:
        try: 
            user_to_delete = RegisteredUser.objects.get(username=username)
            user_to_delete.delete()
            # Add a success message
            messages.success(request, f"User {username} has been successfully deleted.")
        except RegisteredUser.DoesNotExist:
            return HttpResponse("User does not exist")
        return redirect("list_users_page")



# function that require admin rights
def admin_required(view_func):
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_moderator):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You don't have admin rights")
    return _wrapper

# function that require login rights
def login_required(view_func):
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You need to login")
    return _wrapper


# Create your views here.
def index(request):
    return render(request, "index.html", {"title": "Home page"})

#######################################################################################
@login_required
def create_category(request):
    return HttpResponse("Create category page")

@login_required
def create_event(request):
    return HttpResponse("Create event page")


@admin_required
def admin_view(request):
    return render(request, "admin_temps/admin_page.html", {"title": "Admin page"})






#######################################################################################
def logout_view(request):
    logout(request)
    return redirect("home_page")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
            else:
                return HttpResponse("Invalid login or password")
    else:
        form = LoginForm()

    return render(request, "login_temps/login.html", {"title": "Login page", "form": form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            name = form.cleaned_data.get("name")
            surname = form.cleaned_data.get("surname")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")

            print(username, name, surname, email, phone_number, password)

            if email:
               RegisteredUser.create_user(username, name, surname, email, phone_number, password=password)
               user = authenticate(request, username=username, password=password)

               if user is not None:
                   login(request, user)
                   return redirect("home_page")
               else:
                   return HttpResponse("There are some problems with registration. Try again later")
            else:
                return HttpResponse("Invalid email")
    else:
        form = RegisterForm()

    return render(request, "login_temps/register.html", {"title": "Register page", "form": form})

#######################################################################################


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')