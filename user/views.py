from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import LoggedInUser
from django.contrib.auth import get_user_model
from user.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

User = get_user_model() 

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('user:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:user_info')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def user_info(request):
    try:
        user = User.objects.get(username=request.user.username)
        context = {
            'username' : user.username,
            'first_name' : user.first_name or "not set",
            'last_name' : user.last_name,
            'email' : user.email or "Email",
            'phone_number': getattr(user, 'phone_number', 'Phone number'),
            'domicile': getattr(user, 'domicile', 'Domicile')
        }
        return render(request, 'user.html', context)
    except User.DoesNotExist:
        return redirect('user:login')

@csrf_exempt
def update_profile(request):
    form = UserForm(request.POST or None)

    if request.method == "POST":
        user = request.user
        firstname = request.POST.get("fname")
        if (firstname != ""):
            user.first_name = firstname
        lastname = request.POST.get("lname")
        if (lastname != ""):
            user.last_name = lastname
        email = request.POST.get("email")
        if (email != ""):
            user.email = email
        phonenumber = request.POST.get("phone_number")
        if (phonenumber != ""):
            user.phone_number = phonenumber
        domicile = request.POST.get("domicile")
        if (domicile != ""):
            user.domicile = domicile

        user.save()
        return HttpResponseRedirect(reverse('main:index'))

    context = {'form': form}
    print(context)
    return render(request, "user.html", context)

def update_profile_form(request):
    form = UserForm(request.POST or None)
    context = {'form': form}

    return render(request, 'profileform.html', context)

#login required
def logout_user(request):
    logout(request)
    return redirect('user:login')