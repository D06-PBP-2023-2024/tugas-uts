from django.urls import path
import main.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path("author/<int:author_id>", views.author_details, name="author"),
    path("book/<int:book_id>", views.book_details, name="book_details"),
    path("api/books", views.get_books, name="get_all_books"),
    path('result/', views.search_result, name='search_result'),
    path('tags/', views.group_tags, name='group_tags'),
    path('search/', views.search_form, name='search_form'),
    path('search-ajax/', views.search_result_ajax, name='search_result_ajax'),
    path('book/<int:book_id>/comment/', views.comment_book, name='comment_book'),
    path('like/<int:book_id>/', views.like_book, name='like_book'),
    path('reading_list/<int:book_id>/', views.add_reading_list, name='add_reading_list'),
]


