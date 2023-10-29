from django.forms import ModelForm
from main.models import Comment, Tag, Book

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['subject']