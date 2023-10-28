from django.shortcuts import render, get_object_or_404, redirect
from main.models import Book, Tag, Author, Like, Comment, ReadingList
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import django.core.serializers as serializers
from main.forms import CommentForm 


# Create your views here.
def index(request: HttpRequest):
    page = int(request.GET.get("page", 1))
    book_list = Book.objects.all().order_by("title")
    paginator = Paginator(book_list, 8)
    page_obj = paginator.get_page(page)
    context = {
        "page": page,
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)

def author_details(request: HttpRequest, author_id: int):
    author = Author.objects.get(id=author_id)
    author.name = " ".join(author.name.split(",")[::-1])
    context = {
        "author": author,
        "books": author.book_set.all().filter(author=author),
    }
    return render(request, "author_details.html", context)

def book_details(request: HttpRequest, book_id: int):
    book = Book.objects.get(id=book_id)
    context = {
        "book": book,
        "tags": book.tags.all(),
        "author": book.author,
    }
    return render(request, "book_details.html", context)

def get_books(request: HttpRequest):
    limit = 8
    page = int(request.GET.get("page", 1))
    books = Book.objects.all()[(page - 1)*limit:page*limit]
    serializers.serialize("json", books)
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

def search_result(request):
    title = request.POST.get("title")
    tags = request.POST.get("tags")

    if tags != "":
        tag = Tag.objects.filter(subject__contains=tags).first()
 
    books = None
    if title != "":
        books = Book.objects.filter(title__contains=title)
    if books is None and tags != "" and tag is not None:
        books = Book.objects.filter(tags=tag)
    elif books and tags != "" and tag is not None:
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

@csrf_exempt
def search_result_ajax(request):
    title = request.POST.get("title") or ""
    tags = request.POST.get("tags") or ""
    if title == "":
        title = request.GET.get("title") or ""

    if tags != "":
        tag = Tag.objects.filter(subject__contains=tags).first()

    books = None
    if title != "":
        books = Book.objects.filter(title__contains=title)
    if books is None and tags != "" and tag is not None:
        books = Book.objects.filter(tags=tag)
    elif books and tags != "" and tag is not None:
        books = books.filter(tags=tag)

    if books is not None:
        books = serializers.serialize('json', books)
    
    context = {
        'books': books,
        'title': title,
        'tags': tags,
    }

    return JsonResponse(context)

def like_book(request, book_id): 
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    
    if Like.objects.filter().exists: 
        Like.objects.filter(user=user, bookd=book).delete()
        liked = False 
    else: 
        Like.objects.create(user=user, book=book)
        liked = True 
    
    response_data = {'liked': liked, 'likes_count': book.likes.count()}
    return JsonResponse(response_data)
    
def comment_book(request, book_id): 
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST': 
        form = CommentForm(request.POST)
        if form.is_valid(): 
            comment = form.save(commit=False)
            comment.book = book 
            comment.user = request.user 
            comment.save()
            return redirect('main:book_details', book_id=book.id)
    else: 
        form = CommentForm()
    
    context = {
        'form': form, 
        'book': book,
    }
    
    return render(request, 'comment_form.html', context)

def add_reading_list(request, book_id): 
    book = get_object_or_404(Book, pk=book_id)
    request.user.reading_list_books.add(book)