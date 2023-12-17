from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('info/', user_info, name='user_info'),
    path('info/<str:username>/', check_user_info, name="check_user_info"),
    path('user-not-found', user_not_found, name="user_not_found"),
    path('update-profile', update_profile, name='update_profile'),
    path('liked-books/', liked_book_json, name='liked_book'),
    path('comment-books/', comment_book_json, name='comment_book'),
    path('readinglist-books/', readinglist_json, name='readinglist_book'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('info/', user_info, name='user_info'),
    path('json/', user_json, name='user_json'),
    path('logout-flutter/', logout_flutter, name='logout_flutter'),
    path('update-profile-flutter/', update_profile_flutter, name='update_profile_flutter'),

    path('json2/', user_json_2, name='user_json_2'),
    path('liked-books-2/', liked_book_json2, name='user_like_json'),
    path('comment-books-2/', comment_book_json2, name='user_comment_json'),
    path('readinglist-books-2/', readinglist_json2, name='user_readinglist_json'),
    path('update-profile-flutter-2/', update_profile_flutter2, name='update_profile_flutter_2'),
]