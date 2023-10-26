from django.urls import path
from main.views import show_main
from main.views import search_result
from main.views import group_tags
from main.views import search_form

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('result/', search_result, name='search_result'),
    path('tags/', group_tags, name='group_tags'),
    path('search/', search_form, name='search_form')
]
