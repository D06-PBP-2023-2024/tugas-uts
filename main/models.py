from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    subject = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_url = models.TextField()
    download_count = models.IntegerField()
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title