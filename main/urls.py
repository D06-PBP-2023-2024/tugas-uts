from django.urls import path
from main.views import show_main
from main.views import title_search
from main.views import group_tags
import main.views as views

app_name = 'main'
urlpatterns = [
    path("", views.index, name="index"),
    path("api/books", views.get_books, name="get_books"),
    path('title/<str:title>/', title_search, name='title_search'),
    path('grouptags/', group_tags, name='group_tags'),
]


