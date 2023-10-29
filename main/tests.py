from django.test import TestCase, Client
from main.models import *
from main.forms import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class MainTestCase(TestCase):
    def test_book_models(self):
        author = Author.objects.create(name="Author")
        book = Book()
        book.title = "Book"
        book.download_count = 0
        book.author = author
        book.save()
        b = Book.objects.get(title="Book")
        self.assertEqual(book.title, "Book")
        self.assertEqual(book.author.name, "Author")
        self.assertEqual(book.download_count, 0)
        self.assertEqual(book.__str__(), "Book")

    def test_author_models(self):
        author = Author()
        author.name = "Author"
        author.save()
        a = Author.objects.get(name="Author")
        self.assertEqual(author.name, "Author")
        self.assertEqual(author.__str__(), "Author")

    def test_tag_models(self):
        tag = Tag()
        tag.subject = "Tag"
        tag.save()
        t = Tag.objects.get(subject="Tag")
        self.assertEqual(tag.subject, "Tag")
        self.assertEqual(tag.__str__(), "Tag")

    def test_comment_models(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        user = User.objects.create(username="user")
        comment = Comment()
        comment.comment = "Comment"
        comment.book = book
        comment.user = user
        comment.save()
        c = Comment.objects.get(comment="Comment")
        self.assertEqual(comment.comment, "Comment")
        self.assertEqual(comment.book.title, "Book")
        self.assertEqual(comment.user.username, "user")
    
    def test_like_models(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        user = User.objects.create(username="user")
        like = Like()
        like.book = book
        like.user = user
        like.save()
        l = Like.objects.get(book=book)
        self.assertEqual(like.book.title, "Book")
        self.assertEqual(like.user.username, "user")

    def test_reading_list_models(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        user = User.objects.create(username="user")
        reading_list = ReadingList()
        reading_list.book = book
        reading_list.user = user
        reading_list.save()
        r = ReadingList.objects.get(book=book)
        self.assertEqual(reading_list.book.title, "Book")
        self.assertEqual(reading_list.user.username, "user")

    def test_profile_models(self):
        user = User.objects.create(username="user")
        profile = Profile()
        profile.user = user
        profile.first_name = "First"
        profile.last_name = "Last"
        profile.email = "Email"
        profile.phone_number = "Phone"
        profile.domicile = "Domicile"
        profile.save()
        p = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, "user")
        self.assertEqual(profile.first_name, "First")
        self.assertEqual(profile.last_name, "Last")
        self.assertEqual(profile.email, "Email")
        self.assertEqual(profile.phone_number, "Phone")
        self.assertEqual(profile.domicile, "Domicile")

    def test_book_views(self):
        c = Client()
        response = c.get(reverse("main:get_all_books"))
        self.assertEqual(response.status_code, 200)

    def test_author_views(self):
        author = Author.objects.create(name="Author")
        c = Client()
        response = c.get(reverse("main:author", args=[author.id]))
        self.assertEqual(response.status_code, 200)

    def test_book_details_views(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        c = Client()
        response = c.get(reverse("main:book_details", args=[book.id]))
        self.assertEqual(response.status_code, 200)

    def test_index_views(self):
        c = Client()
        response = c.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)

    def test_create_tag_views(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        c = Client()
        response = c.get(reverse("main:create_tag", args=[book.id]))
        self.assertEqual(response.status_code, 302)

    def test_book_details_logged_in_views(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get(reverse("main:book_details", args=[book.id]))
        self.assertEqual(response.status_code, 200)

    def test_create_tag_logged_in_views(self):
        author = Author.objects.create(name="Author")
        book = Book.objects.create(title="Book", author=author, download_count=0)
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get(reverse("main:create_tag", args=[book.id]))
        self.assertEqual(response.status_code, 200)

def test_get_books(self):
    author = Author.objects.create(name="Author")
    book = Book.objects.create(title="Book", author=author, download_count=0)
    c = Client()
    response = c.get(reverse("main:get_all_books"))
    self.assertEqual(response.status_code, 200)
