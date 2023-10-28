from django.db import models
from django.contrib.auth.models import User

class Feeling(models.Model):
    FEELINGS = [
        ('HA', 'Happy'),
        ('SA', 'Sad'),
        ('EX', 'Excited'),
        ('BO', 'Bored'),
        ('SC', 'Scared'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feeling = models.CharField(max_length=2, choices=FEELINGS)

