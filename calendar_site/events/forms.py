from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from datetime import date
from datetime import datetime
from events.models import EventPlace, Category
import pytz

eastern = pytz.timezone('Europe/Prague')


# form for user to enter as a registered user
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# form for user to change his info
class SettingsForm(forms.Form):
    email = forms.EmailField(max_length=255, required=False)
    phone_number = forms.IntegerField(max_value=999999999999, required=False)
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)


# form for registration
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, validators=[
        RegexValidator(regex=r'^[A-Za-z][A-Za-z0-9_]+$',
                       message='Only letters and numbers are allowed for the "username" field.')])
    name = forms.CharField(validators=[RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                                                      message='Only letters are allowed for the "name" field.')])
    surname = forms.CharField(validators=[RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                                                         message='Only letters are allowed for the "surname" field.')])
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=255)
    phone_number = forms.IntegerField(max_value=999999999999, required=False)


class CategoryForm(forms.Form):
    name = forms.CharField(validators=[RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                                                      message='Only letters are allowed for the "category name" field.')])
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
    city = forms.CharField(validators=[RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                                                      message='Only letters are allowed for the "city" field.')])
    street = forms.CharField(validators=[
        RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž][A-Za-z0-9ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                       message='Only letters and numbers are allowed for the "street" field.')])
    place_name = forms.CharField(validators=[
        RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž][A-Za-z0-9ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                       message='Only letters and numbers are allowed for the "place name" field.')])


# form for event creation
class EventForm(forms.Form):
    name = forms.CharField(validators=[
        RegexValidator(regex=r'^[A-Za-zÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž][A-Za-z0-9ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž\s]+$',
                       message='Only letters and numbers are allowed for the "event name" field.')])

    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                 initial=datetime.now(eastern).date(),
                                 validators=[MinValueValidator(limit_value=datetime.now(eastern).date())])
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                               initial=datetime.now(eastern).date(),
                               validators=[MinValueValidator(limit_value=datetime.now(eastern).date())])
    start_time = forms.TimeField(input_formats=['%H:%M'])
    end_time = forms.TimeField(input_formats=['%H:%M'])
    capacity = forms.IntegerField(min_value=1)
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

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = datetime.now(eastern).date()
        self.fields['end_date'].initial = datetime.now(eastern).date()


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

    credit_card_num = forms.IntegerField(min_value=0, required=True)
    card_code = forms.IntegerField(min_value=0, validators=[MaxValueValidator(9999)], required=True)
    expiry_date = forms.DateField(input_formats=['%m/%Y'], required=True,
                                  widget=forms.DateInput(attrs={'placeholder': 'MM/YYYY'})
                                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set readonly attribute for all fields
        for field_name, field in self.fields.items():
            if field_name not in ['credit_card_num', 'card_code', 'expiry_date']:
                self.fields[field_name].widget.attrs['readonly'] = True
