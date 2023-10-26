from django.urls import path
from main.views import title_search
from main.views import group_tags
import main.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path('title/<str:title>/', title_search, name='title_search'),
    path('grouptags/', group_tags, name='group_tags'),
    path("api/books", views.get_books, name="get_all_books"),
    path("book/<int:book_id>", views.book_details, name="book_details")
]


