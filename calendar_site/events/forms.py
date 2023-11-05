from django import forms

from events.models import EventPlace

class LoginForm(forms.Form): 
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone_number = forms.CharField()


class EventForm(forms.Form):
    name = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField(input_formats=['%H:%M'])
    end_time = forms.TimeField(input_formats=['%H:%M'])
    capacity = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    ticket_price = forms.IntegerField()
    place = forms.ModelChoiceField(
        queryset=EventPlace.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    photo = forms.ImageField(required=False)