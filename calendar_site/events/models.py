from django.db import models
from django import forms

# TODO: Если что, название этих моделей в Датабазе начинается с events_ 
# TODO: то есть, есть модель Worker, а в базе она называется events_worker
# TODO: это немного не удобно, но я не знаю, как это исправить

# represents "Registrovany uzivatel" from the ER diagram
class RegisteredUser(models.Model):
    login = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.login


# represents "Zamestnanec" from the ER diagram
class Worker(models.Model):
    # create only two possible choices of the roles of workers
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Moderator', 'Moderator')
    ]
    worker = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


# represents "Misto konani" from the ER diagram
class EventPlace(models.Model):
    place_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10, null=True)
    place_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to=f"Photos/places/{place_id}/%y/%m/%d/", null=True)
    # foreign key represents the "Navrhl" relation from the ERD
    created = models.ForeignKey(RegisteredUser,
                                on_delete=models.CASCADE, related_name='event_place_created')  # how to make creation ???? - in the moment of creation by user?
    # foreign key represents the "Schvalil" relation from the ERD
    accepted = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True,
                                 blank=True, related_name='event_place_accepted')  # how to make accepting ???? after the moment of creation by user?


# represents "Udalost" from the ER diagram
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False, default='2021-01-01')
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=False, default='12:30') # А что если ивент будет длится несколько дней? или 24 часа или весь день просто???
    end_time = models.TimeField(null=True)
    capacity = models.IntegerField()
    ticket_price = models.IntegerField()
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to=f"Photos/events/{event_id}/%y/%m/%d/")

    # foreign key represents the "Kona se" relation from the ERD
    event_place = models.ForeignKey(EventPlace, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_event_place')

    # foreign key represents the "zalozil" relation from the ERD
    created = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='event_created')  # how to make creation ???? - in the moment of creation by user?

    # foreign key represents the "Schvalil" relation from the ERD
    accepted = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True, related_name='event_accepted')  # how to make accepting ???? - after the moment of creation by  user?

    # Many-to-many represents the "Patri" relation from the ERD
    category = models.ManyToManyField('Category')

    # Many-to-many represents the "Registrovan" relation from the ERD
    registered_people = models.ManyToManyField(RegisteredUser)


# represents "Kategorie" from the ER diagram
class Category(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='category_subcategory')

    def __str__(self):
        return self.name


# represents "Hodnoceni" from the ER diagram
class EventEstimation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_estimation_event')
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='event_estimation_user')
    estimation = models.IntegerField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ])
    comment = models.TextField(null=True)

    class Meta:
        # create a primary key pair
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='event_estimation')
        ]


# represents "Uhrada vstupneho" from the ER diagram
class TicketPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_payment_event')
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='ticket_payment_user')
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    ticket_price = models.IntegerField()
    accepted = models.ForeignKey(RegisteredUser, on_delete=models.RESTRICT, null=True,
                                 blank=True)  # event creator accepts the payment only after confirmation

    class Meta:
        # create a primary key pair
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='ticket_payment')
        ]