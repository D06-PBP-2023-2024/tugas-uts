from django.urls import path
from . import views

app_name = 'reading_forum'

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/<int:discussion_id>/<str:filter>/', views.discussion_detail, name='discussion_detail_filtered'),
    path('create-discussion/', views.create_discussion, name='create_discussion'),
    path('discussion/<int:discussion_id>/reply/', views.create_reply, name='create_reply'),
    path('reply_form/<int:discussion_id>/', views.reply_form, name='reply_form'),
    
]