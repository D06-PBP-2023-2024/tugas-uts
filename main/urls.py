from django.urls import path
import main.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path("author/<int:author_id>", views.author_details, name="author"),
    path("book/<int:book_id>", views.book_details, name="book_details"),
    path("api/books", views.get_books, name="get_all_books"),
    path('result/', views.search_result, name='search_result'),
    path('tags/', views.group_tags, name='group_tags'),
    path('tags-ajax/', views.group_tags_json, name='group_tags_json'),
    path('search/', views.search_form, name='search_form'),
    path('search-ajax/', views.search_result_ajax, name='search_result_ajax'),
    path('search-ajax-flutter/', views.search_result_ajax_flutter, name='search_result_ajax_flutter'),
    path('book/<int:book_id>/comment/', views.comment_book, name='comment_book'),
    path('like/<int:book_id>/', views.like_book, name='like_book'),
    path('reading_list/<int:book_id>/', views.add_reading_list, name='add_reading_list'),
    path('book/<int:id>/create_tag/', views.create_tag, name='create_tag'),
    path('create-comment-ajax/<int:book_id>/', views.create_comment_by_ajax, name='create_comment_ajax'),
    path('json_rl/', views.json_rl, name='json_reading_list'),
    path('json_cm/', views.json_cm, name='json_comment'),
]


