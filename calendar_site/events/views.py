from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from events.models import RegisteredUser, EventPlace, Event, Worker, Category, EventEstimation, TicketPayment
from .forms import LoginForm, RegisterForm, EventForm, CommentForm, CategoryForm, PlaceForm, PaymentForm
from django.contrib import messages
from datetime import date
import pytz
from datetime import datetime


# function that delete user from database by username
def delete_user(request, username):
    # get the user that we want to delete
    try:
        user_to_delete = RegisteredUser.objects.get(username=username)
    except:
        return HttpResponse("User does not exist")

    # Check if user is authenticated and has admin rights
    if request.user.is_authenticated and request.user.is_admin:
        # Check if the user that we want to delete is admin
        if user_to_delete.is_admin:
            messages.warning(request, "You cannot delete another admin.")
        elif user_to_delete == request.user:
            messages.warning(request, "You cannot delete yourself.")
        else:
            user_to_delete.delete()
            messages.success(request, f"User {username} has been successfully deleted.")
    else:
        messages.warning(request, "You do not have permission to delete users.")

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


# function that checks if events from the given list are ended
def event_is_ended(events):
    events_ended = []
    eastern = pytz.timezone('Europe/Prague')

    for event in events:
        event_end_date = event.end_date.strftime('%Y-%m-%d')
        event_end_time = event.end_time.strftime('%H:%M:%S')
        today = datetime.now(eastern).date().strftime("%Y-%m-%d")
        today_time = datetime.now(eastern).time().strftime("%H:%M:%S")
        ended = (event_end_date == today and today_time > event_end_time) or event_end_date < today
        events_ended.append(ended)
    return events_ended


# shows main page
def index(request):
    events = Event.objects.all()
    events_ended = event_is_ended(events)
    categories = Category.objects.all()
    return render(request, "index.html",
                  {"title": "Home page", "events": zip(events, events_ended), "categories": categories})


# constructs page "My calendar" with events where user is enrolled
@login_required
def my_calendar(request):
    today_date = datetime.now()
    today_time = datetime.now().time()
    context = {
        "title": "My calendar page",
        "events": Event.objects.all(),
        "categories": Category.objects.all(),
        "places": EventPlace.objects.all(),
        "current_date": today_date.strftime("%Y-%m-%d"),
        "current_time": today_time.strftime("%H:%M:%S")
    }
    return render(request, "my_calendar.html", context)


# shows list of places(unapproved/approved) on the "Admin panel" page
@moderator_required
def list_places(request):
    places = EventPlace.objects.all()
    return render(request, "admin_temps/list_places.html", {"title": "List of places", "places": places})


# shows list of events(unapproved/approved) on the "Admin panel" page
@moderator_required
def list_events(request):
    events = Event.objects.all()
    return render(request, "admin_temps/list_events.html", {"title": "List of events", "events": events})


# shows list of users on the "Admin panel" page
@admin_required
def list_users(request):
    users = RegisteredUser.objects.all()
    return render(request, "admin_temps/list_users.html", {"title": "List of users", "users": users})


# shows list of categories(unapproved/approved) on the "Admin panel" page
@moderator_required
def list_categories(request):
    categories = Category.objects.all()
    return render(request, "admin_temps/list_categories.html",
                  {"title": "List of categories", "categories": categories})


# allows a user to create a place
@login_required
def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            street = form.cleaned_data.get("street")
            place_name = form.cleaned_data.get("place_name")

            # check if place is unique
            if EventPlace.objects.filter(city=city, street=street).exists():
                return HttpResponse("Place with this name already exists")

            event_place = EventPlace(city=city, street=street, place_name=place_name, created=request.user)
            event_place.save()
            # Add a success message
            messages.success(request, f"Place {city} {street} has been successfully sent for approval. ")
            return redirect("home_page")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = PlaceForm()

    places = EventPlace.objects.all()
    context = {
        "title": "Create place page",
        "form": form,
        "places": places
    }

    return render(request, "create_place.html", context)


# allows a user to create a category
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
            if subcategory == None:
                new_category = Category.objects.create(name=name)
                new_category.save()
            elif subcategory != None:
                new_category = Category.objects.create(name=name, subcategory=subcategory)
                new_category.save()
            else:
                return HttpResponse("Something went wrong during category creation")
            # Add a success message
            messages.success(request, f"Category {name} has been successfully sent for approval. ")
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


# allows a user to join to an event(free)
@login_required
def join_user_event(request, event_id, username):
    if request.user.is_authenticated:
        try:
            user = RegisteredUser.objects.get(username=username)
            event = Event.objects.get(pk=event_id)
            event.registered_people.add(user)
            event.save()
            messages.success(request, f"You have been successfully enrolled to the {event.name} event.")
        except RegisteredUser.DoesNotExist:
            return HttpResponse("User does not exist")
        return redirect("home_page")


# help function for event data extraction
def get_data_event_page(event_id, username, form):
    event = Event.objects.get(pk=event_id)
    reg_users_count = len(event.registered_people.all())
    created = str(event.created)
    username = str(username)

    all_event_comments = EventEstimation.objects.filter(event__pk=event_id)

    leaved_comments = [(com.event.pk, com.user.username) for com in EventEstimation.objects.all()]
    can_leave_comment = (event.pk, username) not in leaved_comments and username != event.created.username
    event_ended = event_is_ended([event])[0]

    context = {"event": event, "enrolled_people": reg_users_count,
               "created": created, "username": username,
               "event_is_ended": event_ended, "can_leave_comment": can_leave_comment,
               "all_event_comments": all_event_comments, "form": form}
    return context


# function is responsible for event page showing
def show_event_page(request, event_id):
    form = CommentForm()
    context = get_data_event_page(event_id, request.user.username, form)

    # Check if event is approved by moderator
    if not context["event"].approved_by_mods:
        return HttpResponse("Event is not approved by moderator")

    return render(request, 'event_page.html', context)


# filters events on the main page by selected category
def filter_by_category(request, cat_id):
    events: Event = Event.objects.all()
    categories = Category.objects.all()

    subcats_arr = [Category.objects.filter(subcategory__pk=cat_id)]
    for subcats in subcats_arr:
        for cat in subcats:
            subcats_arr.append(Category.objects.filter(subcategory__pk=cat.pk))

    subcats_arr = [i.pk for arr in subcats_arr for i in arr]
    subcats_arr.append(cat_id)

    filtered_events = []
    for event in events:
        [filtered_events.append(event) for cat in event.categories.all() if cat.pk in subcats_arr]

    events_ended = event_is_ended(filtered_events)
    return render(request, "index.html",
                  {"title": "Home page", "events": zip(filtered_events, events_ended), "categories": categories})


# make payment to enroll in an event(paid)
@login_required
def make_payment(request, event_id, username):
    event: Event = Event.objects.get(pk=event_id)
    user: RegisteredUser = RegisteredUser.objects.get(pk=username)
    ticket_price = event.ticket_price

    eventname = event.name
    user_firstname = user.first_name
    user_lastname = user.last_name
    context = {
        "eventname": eventname,
        "username": username,
        "user_firstname": user_firstname,
        "user_lastname": user_lastname,
        "price": ticket_price,
    }
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            payment = TicketPayment(event=event, user=user, ticket_price=ticket_price)
            payment.save()
            event.registered_people.add(user)
            # Add a success message
            messages.success(request, f"You have been successfully enrolled to the {event.name} event.")
            return redirect("home_page")
        else:
            print("Form is not valid")
            print(form.errors)
            context["form"] = form
            return render(request, "payment_page.html", context)
    else:
        form = PaymentForm()

    context["form"] = form
    return render(request, "payment_page.html", context)


# allow user to leave a comment after event is ended
@login_required
def leave_comment(request, event_id, username):
    event = Event.objects.get(pk=event_id)
    user = RegisteredUser.objects.get(username=username)

    if (event_id, username) in EventEstimation.objects.all():
        return HttpResponse("You have already leaved a comment.")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            print("Comment form is valid\n")
            content = form.cleaned_data.get("content")
            estimation = form.cleaned_data.get("estimation")

            comment = EventEstimation(event=event, user=user, comment=content, estimation=estimation)
            comment.save()
            messages.success(request, f"Your comment was successfully saved.")
            return redirect(f"/events/{event_id}/")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CommentForm()
    context = get_data_event_page(event_id, request.user.username, form)
    return render(request, "event_page.html", context)


# allow moderator/admin to delete comment of a user
@moderator_required
def delete_comment(request, event_id, username):
    EventEstimation.objects.filter(event__pk=event_id, user__username=username).delete()
    form = CommentForm()
    context = get_data_event_page(event_id, username, form)
    return render(request, 'event_page.html', context)


# allows creator of event to list all registered users
@login_required
def list_enrolled_users(request, event_id):
    event = Event.objects.get(pk=event_id)
    reg_users = list(event.registered_people.all())
    return render(request, 'list_enrolled_people.html', {"enrolled_people": reg_users})


# allows a user to create an event
@login_required
def create_event(request):
    event_places = EventPlace.objects.all()
    categires = Category.objects.all()
    context = {
        "title": "Create event page",
        "event_places": event_places,
        "categories": categires
    }
    # initial_data = {"start_date": date.today(), "end_data": date.today(), "start_time": datetime.now().time(),
    #                 "end_time": datetime.now().time()}
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
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
            payment_type = form.cleaned_data.get("payment_type")

            # Add categories from checkboxes
            categories = form.cleaned_data.get("categories")

            # If payment type is free, then ticket price is automatically 0
            if payment_type == "free":
                ticket_price = 0
            elif payment_type == "paid" and ticket_price is None:
                return HttpResponse("You need to specify ticket price")

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
            # Add categories from checkboxes
            for category in categories:
                event.categories.add(Category.objects.get(name=category.name))

            event.save()
            # Add a success message
            messages.success(request, f"Event {name} has been sent for approval.")

            return redirect("home_page")

        else:
            print("Form is not valid")
            print(form.errors)

            context["form"] = form
            context["ev_name"] = form.cleaned_data.get("name")
            context["capacity"] = form.cleaned_data.get("capacity")
            context["description"] = form.cleaned_data.get("description")
            context["ticket_price"] = form.cleaned_data.get("ticket_price")

            return render(request, "create_event.html", context)
    else:
        form = EventForm()
        context["form"] = form

    return render(request, "create_event.html", context)


# shows page for admins/moders
@moderator_required
def admin_view(request):
    return render(request, "admin_temps/admin_page.html", {"title": "Admin page"})


# function allows admins/moders to approve created place by a user
@moderator_required
def approve_place(request, place_id):
    try:
        place = EventPlace.objects.get(place_id=place_id)
        place.approved_by_mods = True
        place.accepted = Worker.objects.get(worker=request.user)
        place.save()
        # Add a success message
        messages.success(request, f"Place {place.place_name} has been successfully approved.")
    except EventPlace.DoesNotExist:
        return HttpResponse("Place does not exist")
    return redirect("list_places_page")


# function allows admins/moders to reject created place by a user
@moderator_required
def reject_place(request, place_id):
    try:
        place = EventPlace.objects.get(place_id=place_id)
        place.approved_by_mods = False
        place.accepted = Worker.objects.get(worker=request.user)
        place.save()
        # Add a success message
        messages.success(request, f"Place {place.place_name} has been successfully rejected.")
    except EventPlace.DoesNotExist:
        return HttpResponse("Place does not exist")
    return redirect("list_places_page")


# function allows admins/moders to approve created category by a user
@moderator_required
def approve_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.approved_by_mods = True
        category.accepted = Worker.objects.get(worker=request.user)
        category.save()

        form = CategoryForm()
        form.update_choices()
        # Add a success message
        messages.success(request, f"Category {category.name} has been successfully approved.")
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist")
    return redirect("list_categories_page")


# function allows admins/moders to reject created category by a user
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


# function allows admins/moders to approve created event by a user
@moderator_required
def approve_event(request, event_id):
    try:
        event: Event = Event.objects.get(event_id=event_id)
        event.registered_people.add(event.created)

        event.approved_by_mods = True
        event.accepted = Worker.objects.get(worker=request.user)
        event.save()
        # Add a success message
        messages.success(request, f"Event {event.name} has been successfully approved.")
    except Event.DoesNotExist:
        return HttpResponse("Event does not exist")
    return redirect("list_events_page")


# function allows admins/moders to reject created event by a user
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


# allow user to log out from his account
def logout_view(request):
    logout(request)
    return redirect("home_page")


# allows user to log in to his account from a corresponding page
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


# allows to create a new account for a new user from a corresponding page
def register_view(request):
    context = {"title": "Register page"}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            name = form.cleaned_data.get("name")
            surname = form.cleaned_data.get("surname")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")

            if len(RegisteredUser.objects.filter(username=username)) != 0:
                return HttpResponse("User with this name already exists.")

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
            print(form.errors)
            context["form"] = form
            context["user_n"] = form.cleaned_data.get("username")
            context["name"] = form.cleaned_data.get("name")
            context["surname"] = form.cleaned_data.get("surname")
            context["phone_num"] = form.cleaned_data.get("phone_number")
            return render(request, "login_temps/register.html", context)
    else:
        form = RegisterForm()
    context["form"] = form
    return render(request, "login_temps/register.html", context)


# runs when there is an unknown page
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
