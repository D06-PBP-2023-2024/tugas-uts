from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('info/', user_info, name='user_info'),
    path('update-profile', update_profile, name='update_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('info/', user_info, name='user_info'),
]