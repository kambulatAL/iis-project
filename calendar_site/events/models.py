from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

default_pass = 'user_pass'


# table represents registered user
class RegisteredUser(AbstractUser):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True)

    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def create_user(username, name, surname, email, phone_number, is_admin=False, is_moderator=False,
                    password=default_pass):
        user = RegisteredUser.objects.create_user(username=username, password=password)
        user.first_name = name
        user.last_name = surname
        user.phone_number = phone_number
        user.email = email
        user.is_admin = is_admin
        user.is_moderator = is_moderator
        user.save()
        if is_admin:
            Worker.objects.create(worker=user, role='Admin')
        elif is_moderator:
            Worker.objects.create(worker=user, role='Moderator')


# table represents admin or moderator
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
    place_name = models.CharField(max_length=255, null=True)
    # foreign key represents the "Navrhl" relation from the ERD
    created = models.ForeignKey(RegisteredUser,
                                on_delete=models.CASCADE,
                                related_name='event_place_created')
    # foreign key represents the "Schvalil" relation from the ERD
    accepted = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True,
                                 blank=True,
                                 related_name='event_place_accepted')
    approved_by_mods = models.BooleanField(default=False)


# represents "Kategorie" from the ER diagram
class Category(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='category_subcategory')

    accepted = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='category_accepted')
    approved_by_mods = models.BooleanField(default=False)


# table represents event
class Event(models.Model):
    name = models.CharField(max_length=255, default='Event name')
    event_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False, default='2021-01-01')
    end_date = models.DateField(null=False, default='2021-01-01')

    start_time = models.TimeField(null=False, default='12:30')
    end_time = models.TimeField(null=False, default='12:30')

    capacity = models.IntegerField()
    ticket_price = models.IntegerField(null=True)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to=f"images/events/%y/%m/%d/")

    # foreign key represents the "Kona se" relation from the ERD
    event_place = models.ForeignKey(EventPlace, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='event_event_place')

    # foreign key represents the "zalozil" relation from the ERD
    created = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE,
                                related_name='event_created')  # how to make creation ???? - in the moment of creation by user?

    # foreign key represents the "Schvalil" relation from the ERD
    # this field means accepted by moderator
    accepted = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='event_accepted')  # how to make accepting ???? - after the moment of creation by  user?

    # Many-to-many represents the "Patri" relation from the ERD
    categories = models.ManyToManyField(Category, related_name='event_category')

    # Many-to-many represents the "Registrovan" relation from the ERD
    registered_people = models.ManyToManyField(RegisteredUser)
    approved_by_mods = models.BooleanField(default=False)


# table represents events estimation
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
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # create a primary key pair
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='event_estimation')
        ]


# table represents payment to enroll to an event
class TicketPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_payment_event')
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='ticket_payment_user')
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    ticket_price = models.IntegerField()

    class Meta:
        # create a primary key pair
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='ticket_payment')
        ]
