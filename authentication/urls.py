from django.urls import path
<<<<<<< HEAD
from authentication.views import login, logout, register
=======
from authentication.views import login
>>>>>>> 0baec6089fb8392a73d63c3eaf4c47971176688c

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
<<<<<<< HEAD
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]
=======
]
>>>>>>> 0baec6089fb8392a73d63c3eaf4c47971176688c
