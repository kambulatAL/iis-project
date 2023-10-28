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
Category.objects.create(name='Music')
Category.objects.create(name='Sport')
Category.objects.create(name='All categories')
Category.objects.create(name='Programmer meeting')
Category.objects.create(name='Food')
Category.objects.create(name='Movies')


# Create event places
EventPlace.objects.create(
    city='Prague',
    street='Vodickova',
    house_number='12',
    place_name='Kino',
    description='A nahuya tak mnogo fields v modeli?',
    photo='',
    # Это нам точно надо??????????????????????
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00'))
)

# Create event places
EventPlace.objects.create(
    city='Brno',
    street='Skacelova',
    house_number='37',
    place_name='Kebab house',
    description='Kebab party',
    photo='',

    # Это нам точно надо??????????????????????
    created=RegisteredUser.objects.get(username='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00'))
)

# Create event

event1 = Event.objects.create(
    # Даты и время в формате YYYY-MM-DD
    # НО оно не позволяет записывать мне это, выдает ошибку Камбулат реши это
    # А еще models.py пиздец сложно читается Events, EnetsPlace итд слишком много field 
    start_date="2023-10-20",
    end_date="2023-10-22",
    start_time="14:00",
    end_time="17:00",
    capacity=100,
    ticket_price=20,
    description="Description of Event 1",
    event_place=EventPlace.objects.get(place_id=1),
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00'))
)

event1.category.add(Category.objects.get(name='Music'))
event1.category.add(Category.objects.get(name='Sport'))

event1.registered_people.add(RegisteredUser.objects.get(username='user_login'))
event1.registered_people.add(RegisteredUser.objects.get(username='xassat00'))