from django.urls import path
import main.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path('grouptags/', views.group_tags, name='group_tags'),
    path("api/books", views.get_books, name="get_all_books"),
    path('result/', views.search_result, name='search_result'),
    path('tags/', views.group_tags, name='group_tags'),
    path('search/', views.search_form, name='search_form'),
    path('search-ajax/', views.search_result_ajax, name='search_result_ajax'),
]


