from django.urls import path
from main.views import show_main
from main.views import title_search
from main.views import group_tags

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('title/<str:title>/', title_search, name='title_search'),
    path('grouptags/', group_tags, name='group_tags'),
]
