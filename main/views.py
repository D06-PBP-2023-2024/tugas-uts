from django.shortcuts import render
from main.models import Book, Tag
from django.http import HttpResponse

# Create your views here.
def show_main(request):
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'index.html', context)

def title_search(request, title):
    books = Book.objects.filter(title__contains=title)
    
    context = {
        'books': books,
    }

    return render(request, 'title.html', context)

def group_tags(request):
    tags = Tag.objects.all()

    books_by_tag = {}

    for tag in tags:
        books = Book.objects.filter(tags=tag)
        books_by_tag[tag.subject] = books

    context = {
        'books_by_tag': books_by_tag,
    }

    return render(request, 'group_tags.html', context)

    