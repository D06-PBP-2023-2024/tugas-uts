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

    def test_search_url_is_exist(self):
        response = Client().get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_using_search_template(self):
        response = Client().get('/search/')
        self.assertTemplateUsed(response, 'search_form.html')

    def test_search_with_title(self):
        Book.objects.create(title='Book', download_count=0, author=Author.objects.create(name='Author'))
        response = Client().post('/search/', {'title': 'Book'})
        self.assertEquals(response.status_code, 200)

    def test_search_with_tags(self):
        tag = Tag.objects.create(subject='Tag')
        book = Book.objects.create(title='Book', download_count=0, author=Author.objects.create(name='Author'))
        book.tags.add(tag)
        response = Client().post('/search/', {'tags': 'Tag'})
        self.assertEquals(response.status_code, 200)


    def test_search_with_title_and_tags(self):
        tag = Tag.objects.create(subject='Tag')
        book = Book.objects.create(title='Book', download_count=0, author=Author.objects.create(name='Author'))
        book.tags.add(tag)
        # post with formdata
        response = Client().post('/search/', {'title': 'Book', 'tags': 'Tag'})
        self.assertEquals(response.status_code, 200)

    def test_group_tags(self):
        response = Client().get('/tags/')
        self.assertEquals(response.status_code, 200)

    def test_search_form(self):
        response = Client().get('/search/')
        self.assertEquals(response.status_code, 200)

    def test_comment_form(self):
        response = Client().get('/book/1/comment/')
        self.assertEquals(response.status_code, 302)

    def test_comment_form_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get('/book/1/comment/')
        self.assertEquals(response.status_code, 200)
    
    def test_like_book(self):
        response = Client().get('/like/1/')
        self.assertEquals(response.status_code, 302)

    def test_like_book_twice(self):
        response = Client().get('/like/1/')
        response = Client().get('/like/1/')
        self.assertEquals(response.status_code, 302)

    def test_like_book_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get('/like/1/')
        self.assertEquals(response.status_code, 200)

    def test_like_twice_book_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get('/like/1/')
        response = c.get('/like/1/')
        self.assertEquals(response.status_code, 200)

    def test_add_reading_list(self):
        response = Client().get('/reading_list/1/')
        self.assertEquals(response.status_code, 302)

    def test_add_reading_list_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get('/reading_list/1/')
        self.assertEquals(response.status_code, 302)

    def test_post_comment_with_form_data(self):
        response = Client().post('/book/1/comment/', {'comment': 'Comment'})
        self.assertEquals(response.status_code, 302)

    def test_post_comment_with_form_data_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.post('/book/1/comment/', {'comment': 'Comment'})
        self.assertEquals(response.status_code, 302)

    def test_add_reading_list_twice_with_login(self):
        user = User.objects.create(username="user")
        user.set_password("password")
        user.save()
        c = Client()
        c.login(username="user", password="password")
        response = c.get('/reading_list/1/')
        response = c.get('/reading_list/1/')
        self.assertEquals(response.status_code, 302)