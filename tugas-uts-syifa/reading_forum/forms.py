from django import forms
from .models import Discussion, Reply

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
