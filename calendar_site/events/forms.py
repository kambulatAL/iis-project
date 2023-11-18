from django import forms

from events.models import EventPlace, Category


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


class CategoryForm(forms.Form):
    name = forms.CharField()
    subcategory = forms.ChoiceField(
        choices=[(None, 'None')] + [(category.name, category.name) for category in Category.objects.all()],
        required=False
    )

    def __init__ (self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].choices += [(category.name, category.name) for category in Category.objects.all()]

    # Function that update category choices in the form after adding new category
    def update_choices(self):
        self.fields['subcategory'].choices = [(None, 'None')] + [(category.name, category.name) for category in Category.objects.all()]


class PlaceForm(forms.Form):
    city = forms.CharField()
    street = forms.CharField()
    place_name = forms.CharField()


class EventForm(forms.Form):
    name = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField(input_formats=['%H:%M'])
    end_time = forms.TimeField(input_formats=['%H:%M'])
    capacity = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    ticket_price = forms.IntegerField(min_value=0)

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


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    estimation = forms.ChoiceField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ], widget=forms.RadioSelect)


class PaymentForm(forms.Form):

    eventname = forms.CharField()
    userlogin = forms.CharField()
    user_firstname = forms.CharField()
    user_lastname = forms.CharField()
    ticket_price = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set readonly attribute for all fields
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].required = False
