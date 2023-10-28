from django.contrib import admin
from main.models import Book, Author, Tag

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Tag)