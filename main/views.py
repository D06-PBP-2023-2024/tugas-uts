from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from main.models import Book, Tag
from django.core.paginator import Paginator

# Create your views here.
def index(request: HttpRequest):
    page = int(request.GET.get("page", 1))
    book_list = Book.objects.all().order_by("-download_count")
    paginator = Paginator(book_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        "page": page,
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)

def book_details(request: HttpRequest, book_id: int):
    book = Book.objects.get(id=book_id)
    context = {
        "book": book,
    }
    return render(request, "book_details.html", context)

def get_books(request: HttpRequest):
    limit = 10
    page = int(request.GET.get("page", 1))
    books = Book.objects.all()[(page - 1)*limit:page*limit]
    serializers.serialize("json", books)
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")


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

    
