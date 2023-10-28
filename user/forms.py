from django.forms import ModelForm
from main.models import LoggedInUser

class UserForm(ModelForm):
    class Meta:
        model = LoggedInUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'domicile']