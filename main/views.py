from django.shortcuts import render
from main.models import Book
from django.http import HttpResponse

# Create your views here.
def show_main(request):
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, "index.html", context)