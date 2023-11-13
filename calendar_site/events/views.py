from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from events.models import RegisteredUser, EventPlace, Event, Worker, Category
from .forms import LoginForm, RegisterForm, EventForm, CategoryForm
from django.contrib import messages


############################################################################################### Admin functions

# function that delete user from database by username
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


# function that require moderator rights
def moderator_required(view_func):
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_moderator):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You don't have moderator rights")

    return _wrapper


# function that require admin rights
def admin_required(view_func):
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
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


def index(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    return render(request, "index.html", {"title": "Home page", "events": events, "categories": categories})


@moderator_required
def list_places(request):
    places = EventPlace.objects.all()
    return render(request, "admin_temps/list_places.html", {"title": "List of places", "places": places})


@moderator_required
def list_events(request):
    events = Event.objects.all()
    return render(request, "admin_temps/list_events.html", {"title": "List of events", "events": events})


# Make sure, that user is admin
@admin_required
def list_users(request):
    users = RegisteredUser.objects.all()
    return render(request, "admin_temps/list_users.html", {"title": "List of users", "users": users})


@moderator_required
def list_categories(request):
    categories = Category.objects.all()
    return render(request, "admin_temps/list_categories.html",
                  {"title": "List of categories", "categories": categories})


#######################################################################################
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            subcategory = form.cleaned_data.get("subcategory")
            # check if name is unique
            if Category.objects.filter(name=name).exists():
                return HttpResponse("Category with this name already exists")

            if subcategory == "None":
                new_category = Category.objects.create(name=name)
                new_category.save()
            elif subcategory != "None":
                new_category = Category.objects.create(name=name, subcategory=Category.objects.get(name=subcategory))
                new_category.save()
            else:
                return HttpResponse("Something went wrong during category creation")
            # Add a success message
            messages.success(request, f"Category {name} has been successfully created. ")
            return redirect("home_page")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CategoryForm()

    category_names = Category.objects.all()
    context = {
        "title": "Create category page",
        "category_names": category_names,
        "form": form
    }
    return render(request, "create_category.html", context)


@login_required
def join_user_event(request, event_id, username):
    if request.user.is_authenticated:
        try:
            user = RegisteredUser.objects.get(username=username)
            event = Event.objects.get(pk=event_id)
            event.registered_people.add(user)
            event.save()
            messages.success(request, f"User {username} has successfully joined to the '{event.name}' event.")
        except RegisteredUser.DoesNotExist:
            return HttpResponse("User does not exist")
        return redirect("home_page")


def show_event_page(request, event_id):
    event = Event.objects.get(pk=event_id)
    reg_users_count = len(event.registered_people.all())
    created = str(event.created)
    username = str(request.user.username)
    return render(request, 'event_page.html',
                  {"event": event, "enrolled_people": reg_users_count, "created": created, "username": username})


def list_enrolled_users(request, event_id):
    event = Event.objects.get(pk=event_id)
    reg_users = list(event.registered_people.all())
    return render(request, 'list_enrolled_people.html', {"enrolled_people": reg_users})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            name = form.cleaned_data.get("name")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            start_time = form.cleaned_data.get("start_time")
            end_time = form.cleaned_data.get("end_time")
            capacity = form.cleaned_data.get("capacity")
            description = form.cleaned_data.get("description")
            ticket_price = form.cleaned_data.get("ticket_price")
            place = form.cleaned_data.get("place")
            photo = form.cleaned_data.get("photo")
            ## TODO: need to add checking if place is not None and etc....
            ## TODO: need to add categories

            event = Event(
                name=name,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                capacity=capacity,
                description=description,
                ticket_price=ticket_price,
                event_place=place,
                created=request.user,
                photo=photo
            )
            event.save()

            # Add a success message
            messages.success(request, f"Event {name} has been sent for approval.")

            return redirect("home_page")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = EventForm()

    event_places = EventPlace.objects.all()
    context = {
        "title": "Create event page",
        "event_places": event_places,
        "form": form
    }

    return render(request, "create_event.html", context)


@moderator_required
def admin_view(request):
    return render(request, "admin_temps/admin_page.html", {"title": "Admin page"})


@moderator_required
def approve_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.approved_by_mods = True
        category.accepted = Worker.objects.get(worker=request.user)
        category.save()
        # Add a success message
        messages.success(request, f"Category {category.name} has been successfully approved.")
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist")
    return redirect("list_categories_page")


@moderator_required
def reject_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.approved_by_mods = False
        category.accepted = Worker.objects.get(worker=request.user)
        category.save()
        # Add a success message
        messages.success(request, f"Category {category.name} has been successfully rejected.")
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist")
    return redirect("list_categories_page")


@moderator_required
def approve_event(request, event_id):
    try:
        event = Event.objects.get(event_id=event_id)
        event.approved_by_mods = True
        event.accepted = Worker.objects.get(worker=request.user)
        event.save()
        # Add a success message
        messages.success(request, f"Event {event.name} has been successfully approved.")
    except Event.DoesNotExist:
        return HttpResponse("Event does not exist")
    return redirect("list_events_page")


@moderator_required
def reject_event(request, event_id):
    try:
        print(request.user)
        event = Event.objects.get(event_id=event_id)
        event.approved_by_mods = False
        event.accepted = Worker.objects.get(worker=request.user)
        event.save()
        # Add a success message
        messages.success(request, f"Event {event.name} has been successfully rejected.")
    except Event.DoesNotExist:
        return HttpResponse("Event does not exist")
    return redirect("list_events_page")


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

            if RegisteredUser.objects.filter(username=username).exists():
                return HttpResponse("User with this name already exists.")
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
