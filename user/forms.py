from django.forms import ModelForm
from main.models import LoggedInUser
from user.models import Feeling
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = LoggedInUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'domicile']

class FeelingForm(forms.ModelForm):
    class Meta:
        model = Feeling
        fields = ['feeling']
