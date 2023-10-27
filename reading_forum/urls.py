from django.urls import path
from . import views

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('create-discussion/', views.create_discussion, name='create_discussion'),
    path('discussion/<int:discussion_id>/reply/', views.create_reply, name='create_reply'),
]
