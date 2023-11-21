from django import forms
from django.core.validators import MaxValueValidator

from events.models import EventPlace, Category


# form for user to enter as a registered user
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# form for registration
class RegisterForm(forms.Form):
    username = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone_number = forms.CharField()


class CategoryForm(forms.Form):
    name = forms.CharField()
    subcategory = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='None',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Category.objects.all()

    def update_choices(self):
        self.fields['subcategory'].queryset = Category.objects.all()


# form for place creation
class PlaceForm(forms.Form):
    city = forms.CharField()
    street = forms.CharField()
    place_name = forms.CharField()


# form for event creation
class EventForm(forms.Form):
    name = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField(input_formats=['%H:%M'])
    end_time = forms.TimeField(input_formats=['%H:%M'])
    capacity = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    ticket_price = forms.IntegerField(min_value=0, required=False)
    payment_type = forms.CharField()

    place = forms.ModelChoiceField(
        queryset=EventPlace.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    photo = forms.ImageField(required=False, label='Event photo')
    # Categories that u get from checkboxes
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


# form for writing comment and estimation for an event
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    estimation = forms.ChoiceField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ], widget=forms.RadioSelect)


# form for payment in oder to enroll into event
class PaymentForm(forms.Form):
    eventname = forms.CharField(required=False)
    userlogin = forms.CharField(required=False)
    user_firstname = forms.CharField(required=False)
    user_lastname = forms.CharField(required=False)
    ticket_price = forms.IntegerField(required=False)

    credit_card_num = forms.IntegerField(required=True)
    card_code = forms.IntegerField(validators=[MaxValueValidator(9999)], required=True)
    expiry_date = forms.DateField(input_formats=['%m/%Y'], required=True,
                                  widget=forms.DateInput(attrs={'placeholder': 'MM/YYYY'})
                                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set readonly attribute for all fields
        for field_name, field in self.fields.items():
            if field_name not in ['credit_card_num', 'card_code', 'expiry_date']:
                self.fields[field_name].widget.attrs['readonly'] = True
