from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    path('info/', user_info, name='user_info'),
]