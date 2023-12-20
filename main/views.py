from django.shortcuts import render, get_object_or_404, redirect
from main.models import Book, Tag, Author, Like, Comment, ReadingList
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import django.core.serializers as serializers
from main.forms import CommentForm, TagForm


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


@csrf_exempt
def book_details_json(request: HttpRequest, book_id: int):
    book = Book.objects.get(id=book_id)
    data = book.to_dict()
    data["tags"] = [{"id": tag.pk, "subject": tag.subject}
                    for tag in book.tags.all()]
    data["comments"] = [{"id": comment.pk, "user": comment.user.username, "comment": comment.comment}
                        for comment in book.comment_set.all()]
    data["likes"] = [{"id": like.pk, "user": like.user.username}
                     for like in book.like_set.all()]
    return JsonResponse(data)


def book_details(request: HttpRequest, book_id: int):
    book = Book.objects.get(id=book_id)
    if not request.user.is_authenticated:
        context = {
            "book": book,
            "tags": book.tags.all(),
            "author": book.author,
            "comments": [],
            "likes": book.likes.count(),
            "liked": False,
            'last_login': None,
        }
        response = render(request, "book_details.html", context)
    else:
        context = {
            "book": book,
            "tags": book.tags.all(),
            "author": book.author,
            "comments": Comment.objects.filter(book=book),
            "likes": book.likes.count(),
            "added": ReadingList.objects.filter(user=request.user, book=book).exists(),
            "liked": Like.objects.filter(user=request.user, book=book).exists(),
            'last_login': request.COOKIES['last_login'] if 'last_login' in request.COOKIES else "N/A",
        }
        response = render(request, "book_details.html", context)
        response.set_cookie('last_login', request.user.last_login)
    return response


def get_books(request: HttpRequest):
    limit = 8
    if request.GET.get("page", None) == "all":
        books = Book.objects.prefetch_related("tags", "author").all()

        return HttpResponse(serializers.serialize("json", books), content_type="application/json")
    else:
        page = int(request.GET.get("page", 1))
    books = Book.objects.all()[(page - 1)*limit:page*limit]
    serializers.serialize("json", books)
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")


def search_result(request):
    title = request.POST.get("title")
    tags = request.POST.get("tags")
    # fixed something on search
    if tags != "":
        tag = Tag.objects.filter(subject__contains=tags)
    books = []
    if title != "":
        books = Book.objects.filter(title__contains=title)

    if books == [] and tags != "" and tag != []:
        for tg in tag:
            book = Book.objects.filter(tags=tg)
            books += book

    elif books and tags != "" and tag != [] and title != "":
        filtered_book = []
        for tg in tag:
            book = books.filter(tags__subject__contains=tg)
            filtered_book += book
        books = filtered_book

    context = {
        'books': set(books),
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


def group_tags_json(request):
    tags = Tag.objects.all()

    books_by_tag = {}

    for tag in tags:
        rawbooks = Book.objects.filter(tags=tag)
        books = []
        for book in rawbooks:
            books.append(book.to_dict())

        books_by_tag[tag.subject] = books

    context = {
        'books_by_tag': books_by_tag
    }

    return JsonResponse(context)


def search_form(request):
    context = {}
    return render(request, 'search_form.html', context)


@login_required(login_url="user:login")
@csrf_exempt
def create_comment_by_ajax(request: HttpRequest, book_id):
    if request.method != "POST":
        return JsonResponse({"success": False})
    comment = request.POST.get("comment")
    print(request.POST)
    book = get_object_or_404(Book, pk=book_id)
    Comment.objects.create(user=request.user, book=book, comment=comment)
    return JsonResponse({"success": True})


@csrf_exempt
def search_result_ajax(request):
    title = request.POST.get("title") or ""
    tags = request.POST.get("tags") or ""

    if title == "":
        title = request.GET.get("title") or ""

    # fixed something on search
    if tags != "":
        tag = Tag.objects.filter(subject__contains=tags)

    books = []
    if title != "":
        books = Book.objects.filter(title__contains=title)

    if books == [] and tags != "" and tag != []:
        for tg in tag:
            book = Book.objects.filter(tags=tg)
            books += book

    elif books and tags != "" and tag != [] and title != "":
        filtered_book = []
        for tg in tag:
            book = books.filter(tags__subject__contains=tg)
            filtered_book += book
        books = filtered_book

    if books != []:
        books = set(books)
        books = serializers.serialize('json', books)

    context = {
        'books': books,
        'title': title,
        'tags': tags,
    }

    return JsonResponse(context)


@csrf_exempt
def search_result_ajax_flutter(request):
    title = request.POST.get("title") or ""
    tags = request.POST.get("tags") or ""

    if title == "":
        title = request.GET.get("title") or ""

    # fixed something on search
    if tags != "":
        tag = Tag.objects.filter(subject__contains=tags)

    books = []
    if title != "":
        books = Book.objects.filter(title__contains=title)

    if books == [] and tags != "" and tag != []:
        for tg in tag:
            book = Book.objects.filter(tags=tg)
            books += book

    elif books and tags != "" and tag != [] and title != "":
        filtered_book = []
        for tg in tag:
            book = books.filter(tags__subject__contains=tg)
            filtered_book += book
        books = filtered_book

    if books != []:
        books = set(books)
        send_book = []
        for book in books:
            send_book.append(book.to_dict())
    else:
        send_book = []

    context = {
        'books': send_book,
    }

    return JsonResponse(context)

@csrf_exempt
def like_book_flutter(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if Like.objects.filter(user=user, book=book).exists():
        Like.objects.filter(user=user, book=book).delete()
        liked = False
    else:
        Like.objects.create(user=user, book=book)
        liked = True

    response_data = {'liked': liked, 'likes_count': book.likes.count()}
    return JsonResponse(response_data)

@login_required(login_url="user:login")
@csrf_exempt
def like_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if Like.objects.filter(user=user, book=book).exists():
        Like.objects.filter(user=user, book=book).delete()
        liked = False
    else:
        Like.objects.create(user=user, book=book)
        liked = True

    response_data = {'liked': liked, 'likes_count': book.likes.count()}
    return JsonResponse(response_data)


@login_required(login_url="user:login")
def create_tag(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            if not Tag.objects.filter(subject=form.cleaned_data['subject']).exists():
                tag: Tag = form.save()
            else:
                tag = Tag.objects.get(subject=form.cleaned_data['subject'])
            tag.books.add(book)
            tag.save()
            book.tags.add(tag)
            book.save()
            return redirect('main:book_details', book_id=book.id)
    else:
        form = TagForm()
    return render(request, 'create_tag.html', {'form': form})


@login_required(login_url="user:login")
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

def comment_book_flutter(request, book_id):
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

    return JsonResponse(context)

@login_required(login_url="user:login")
def add_reading_list(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    rl = ReadingList.objects.filter(user=request.user, book=book)
    if rl.exists():
        rl.delete()
    else:
        ReadingList.objects.create(user=request.user, book=book)
    return redirect('main:book_details', book_id=book.id)

def add_reading_list_flutter(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    rl = ReadingList.objects.filter(user=request.user, book=book)
    
    if rl.exists():
        rl.delete()
        response_data = {'status': 'success', 'message': 'Reading list item removed.'}
    else:
        ReadingList.objects.create(user=request.user, book=book)
        response_data = {'status': 'success', 'message': 'Reading list item added.'}

    return JsonResponse(response_data)