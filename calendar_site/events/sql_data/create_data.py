from events.models import RegisteredUser, Worker, Category, EventPlace, Event, EventEstimation

# Как запустить этот код
# 1. python3 manage.py makemigrations
# 2. python3 manage.py migrate
# 3. python3 manage.py shell < create_data.py


default_pass = 'user_pass'

## Create users
#def create_user(username, name, surname, email, phone_number, is_admin=False, is_moderator=False):
#    default_password = 'user_pass'
#    user = RegisteredUser.objects.create_user(username=username, password=default_password)
#    user.first_name = name
#    user.last_name = surname
#    user.email = email
#    user.save()
#    if is_admin:
#        Worker.objects.create(worker=user, role='Admin')
#    elif is_moderator:
#        Worker.objects.create(worker=user, role='Moderator')


RegisteredUser.create_user('xblanco00', 'Marimba', 'Blanco', 'blanco@work.gmail', 'blanco_phone')
RegisteredUser.create_user('xassat00', 'Dias', 'Assatulla', 'xassat@work.gmail', '+420 777 777 777', is_admin=True)
RegisteredUser.create_user('xapada00', 'Parad', 'Moshi-Moshi', 'xapada@work.gmail', '+420 333 777 777', is_moderator=True)
RegisteredUser.create_user('user_login', 'user_name', 'user_surname', 'user_email', 'user_phone')



# Create default categories
Category.objects.create(
    name='Music',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    #created=RegisteredUser.objects.get(username='xblanco00'),
    approved_by_mods=True
    )
Category.objects.create(
    name='Sport',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    #created=RegisteredUser.objects.get(username='xblanco00'),
    approved_by_mods=True
    )
Category.objects.create(
    name='Programmer meeting',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    #created=RegisteredUser.objects.get(username='xblanco00'),
    approved_by_mods=True
    )
Category.objects.create(
    name='Food',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    #created=RegisteredUser.objects.get(username='xblanco00'),
    approved_by_mods=True
    )
Category.objects.create(
    name='Movies',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    #created=RegisteredUser.objects.get(username='xblanco00'),
    approved_by_mods=True
    )


# Create event places
EventPlace.objects.create(
    city='Prague',
    street='Vodickova',
    place_name='Kino',
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

# Create event places
EventPlace.objects.create(
    city='Olomouc',
    street='Skrzaa',
    place_name='Kino Alaska',
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

# Create event places
EventPlace.objects.create(
    city='Brno',
    street='Skacelova',
    place_name='Kebab house',
    created=RegisteredUser.objects.get(username='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

# Create event

event1 = Event.objects.create(
    name="Event 1",
    start_date="2023-10-20",
    end_date="2023-10-22",
    start_time="14:00",
    end_time="17:00",
    capacity=100,
    ticket_price=20,
    description="Description of Event 1",
    event_place=EventPlace.objects.get(place_id=1),
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

event1.categories.add(Category.objects.get(name='Music'))
event1.categories.add(Category.objects.get(name='Sport'))

event1.registered_people.add(RegisteredUser.objects.get(username='user_login'))
event1.registered_people.add(RegisteredUser.objects.get(username='xassat00'))

event1.save()


event2 = Event.objects.create(
    name="Event 2",
    start_date="2023-10-22",
    end_date="2023-10-23",
    start_time="14:00",
    end_time="17:00",
    capacity=100,
    ticket_price=0,
    description="Description of Event 2",
    event_place=EventPlace.objects.get(place_id=2),
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

event2.categories.add(Category.objects.get(name='Music'))
event2.save()