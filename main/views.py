from django.shortcuts import render
from django.urls import reverse
from main.models import Book, Tag
from django.http import HttpResponseRedirect

# Create your views here.
def show_main(request):
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'index.html', context)

def search_result(request):
    title = request.POST.get("title")
    tags = request.POST.get("tags")

    if tags != "":
        tag = Tag.objects.get(subject=tags)

    books = None
   
    if title != "":
        books = Book.objects.filter(title__contains=title)
    if books is None and tags != "":
        books = Book.objects.filter(tags=tag)
    elif books and tags != "":
        books = books.filter(tags=tag)
    
    context = {
        'books': books,
        'title': title,
        'tags': tags,
    }

    return render(request, 'result.html', context)

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

def search_form(request):

    context = {}

    return render(request, 'search_form.html', context)