from django import forms
from .models import Feeling

class FeelingForm(forms.ModelForm):
    class Meta:
        model = Feeling
        fields = ['feeling']
