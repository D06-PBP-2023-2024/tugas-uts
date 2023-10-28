from django.contrib import admin
from main.models import Book, Author, Tag, Like, Comment, Profile, ReadingList

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(ReadingList)