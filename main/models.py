from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    domicile = models.CharField(max_length=100, blank=True, null=True)

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    subject = models.CharField(max_length=100)
    books = models.ManyToManyField('Book')

    def __str__(self):
        return self.subject

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    
class Comment(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    comment = models.TextField()
    
class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_url = models.TextField()
    download_count = models.IntegerField()
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name='book_likes', through=Like)
    comments = models.ManyToManyField(User, related_name='book_comments', through=Comment)
    reading_list = models.ManyToManyField(User, related_name='reading_list', through=ReadingList)
    
    def to_dict(self):
        return {
            'id': self.id,
            'fields':{
                'title': self.title,
                'author': self.author.name,
                'cover_url': self.cover_url,
            },
            'download_count': self.download_count,
            'content': self.content,
            'tags': list(self.tags.values_list('id', flat=True)),
            'likes': list(self.likes.values_list('id', flat=True)),
            'comments': list(self.comments.values_list('id', flat=True)),
            'reading_list': list(self.reading_list.values_list('id', flat=True)),}

    def __str__(self):
        return self.title