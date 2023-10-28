from django.contrib import admin
from main.models import Book, Author, Tag, Like, Comment

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Comment)