from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('info/', user_info, name='user_info'),
    path('info/<int:id>/', check_user_info, name="check_user_info"),
    path('user-not-found', user_not_found, name="user_not_found"),
    path('update-profile', update_profile, name='update_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('info/', user_info, name='user_info'),
]