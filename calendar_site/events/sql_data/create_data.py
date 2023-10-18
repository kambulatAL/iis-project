from events.models import RegisteredUser, Worker, Category, EventPlace, Event, EventEstimation

# Как запустить этот код
# 1. python3 manage.py makemigrations
# 2. python3 manage.py migrate
# 3. python3 manage.py shell < create_data.py

"""
Этот код добавляет 4 юзера, из которых 2 имеют роль админа и модератора
Также создает 6 категорий и 2 места проведения мероприятий
А также создает 1 мероприятие

Камбулат реши это, слишком дохуя fields, слишком сложно читается, слишком дохуя всего
Либо добавь комментарии к моделям и его првкам
"""

default_pass = 'user_pass'

# Create a user
user = RegisteredUser(login='user_login', name='user_name', surname='user_surname', \
                                            password=default_pass, email='user_email', phone_number='user_phone')
user.save()

# Try to create in one line
RegisteredUser.objects.create(login='xblanco00', name='Marimba', surname='Blanco', \
                                            password=default_pass, email='blanco@work.gmail', phone_number='blanco_phone')

RegisteredUser.objects.create( # This user will have admin role
    login='xassat00',
    name='Dias',
    surname='Assatulla',
    password=default_pass,
    email='xassat@work.gmail',
    phone_number='+420 777 777 777'
)

RegisteredUser.objects.create( # This user will have moderator role
    login='xapada00',
    name='Parad',
    surname='Moshi-Moshi',
    password=default_pass,
    email='xapada@work.gmail',
    phone_number='+420 333 777 777'
)

# Assign roles to users
Worker.objects.create(worker=RegisteredUser.objects.get(login='xassat00'), role='Admin')
Worker.objects.create(worker=RegisteredUser.objects.get(login='xapada00'), role='Moderator')


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
    created=RegisteredUser.objects.get(login='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(login='xassat00'))
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
    created=RegisteredUser.objects.get(login='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(login='xassat00'))
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
    created=RegisteredUser.objects.get(login='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(login='xassat00'))
)

event1.category.add(Category.objects.get(name='Music'))
event1.category.add(Category.objects.get(name='Sport'))

event1.registered_people.add(RegisteredUser.objects.get(login='user_login'))
event1.registered_people.add(RegisteredUser.objects.get(login='xassat00'))