from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from main.models import Book
from django.core.paginator import Paginator

# Create your views here.
def index(request: HttpRequest):
    page = int(request.GET.get("page", 0))
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)  # Show 25 contacts per page.
    page_obj = paginator.get_page(page)
    context = {
        "page": page,
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)

def get_books(request: HttpRequest):
    limit = 10
    page = int(request.GET.get("page", 1))
    books = Book.objects.all()[(page - 1)*limit:page*limit]
    serializers.serialize("json", books)
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")