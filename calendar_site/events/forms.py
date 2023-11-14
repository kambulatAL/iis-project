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

    photo = forms.ImageField(required=False, label='Event photo')

    # Categories that u get from checkboxes
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )