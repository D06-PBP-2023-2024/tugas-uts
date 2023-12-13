from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('info/', user_info, name='user_info'),
    path('info/<str:username>/', check_user_info, name="check_user_info"),
    path('user-not-found', user_not_found, name="user_not_found"),
    path('update-profile', update_profile, name='update_profile'),
    path('liked-books', liked_book_json, name='liked_book'),
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
    path('like-json/', user_like_json, name='user_like_json'),
    path('comment-json/', user_comment_json, name='user_comment_json'),
    path('readinglist-json/', user_readlist_json, name='user_readinglist_json'),
]