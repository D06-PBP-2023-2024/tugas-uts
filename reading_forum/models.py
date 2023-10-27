from django.db import models
from django.contrib.auth.models import User

## model buat represent struktur data per forum post
class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField('Reply', related_name='discussion_replies')

## model buat represent struktur data per reply di certain forum post
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    




