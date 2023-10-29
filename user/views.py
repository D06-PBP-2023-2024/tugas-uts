from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Profile, Like, Comment, Author
from user.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
import json
import random

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logged_in_user = Profile(user=user)
            logged_in_user.save()
            messages.success(request, 'Your account has been successfully created!')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Registration failed. Please try again.'})
    context = {'form':form}
    return render(request, 'register.html', context)

def filter_books(data, download_range):
    min_downloads, max_downloads = download_range.split('-')
    min_downloads = int(min_downloads)
    max_downloads = int(max_downloads) if max_downloads != 'inf' else float('inf')
    return [book for book in data if min_downloads <= book['download_count'] <= max_downloads]

@csrf_exempt
def login_user(request):
    with open('data.json') as f:
        data = json.load(f)

    download_range = request.GET.get('download_range', '0-10000')
    
    filtered_books = filter_books(data, download_range)
    book = random.choice(filtered_books)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Sorry, incorrect username or password. Please try again.'})
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'book': book, 'download_range': download_range})

    context = {'book': book}
    return render(request, 'login.html', context)

@login_required(login_url='user:login')
def user_info(request):
    try:
        user = request.user

        if request.user.is_superuser:
            try:
                logged_in_user = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile(user=user)
                profile.save()

        try:
            logged_in_user = Profile.objects.get(user=user)
            form = UserForm(request.POST or None)
            likes = Like.objects.filter(user=user)
            books_liked = [like.book for like in likes]
            comments = Comment.objects.filter(user=user)
            context = {
                'username' : user.username,
                'first_name' : logged_in_user.first_name or "",
                'last_name' : logged_in_user.last_name or "",
                'email' : logged_in_user.email or "Email",
                'phone_number': logged_in_user.phone_number or "Phone number",
                'domicile': logged_in_user.domicile or "Domicile",
                'liked_books' : books_liked,
                'comments' : comments,
                'form' : form
            }
            return render(request, 'user.html', context)
        except Profile.DoesNotExist:
            return redirect('user:login')
    except User.DoesNotExist:
        return redirect('user:login')
    
def check_user_info(request,username):
    try:
        user = User.objects.get(username=username)
        try:
            logged_in_user = Profile.objects.get(user=user)
            likes = Like.objects.filter(user=user)
            books_liked = [like.book for like in likes]
            comments = Comment.objects.filter(user=user)
            context = {
                'username' : user.username,
                'first_name' : logged_in_user.first_name or "",
                'last_name' : logged_in_user.last_name or "",
                'email' : logged_in_user.email or "Email",
                'phone_number': logged_in_user.phone_number or "Phone number",
                'domicile': logged_in_user.domicile or "Domicile",
                'liked_books' : books_liked,
                'comments' : comments,
            }
            return render(request, "check_user.html", context)
        except Profile.DoesNotExist:
            return redirect('user:user_not_found')
    except User.DoesNotExist:
        return redirect('user:user_not_found')
    
def user_not_found(request):
    return render(request, "user_not_found.html")

def liked_book_json(request):
    user = request.user
    likes = Like.objects.filter(user=user)
    books_liked = []
    for like in likes:
        tmp = {
            "title" : like.book.title,
            "cover_url" : like.book.cover_url,
            "author" : like.book.author.name
        }           
        books_liked.append(tmp)

    return JsonResponse({"books" : books_liked})

@csrf_exempt
def update_profile(request):
    form = UserForm(request.POST or None)
    user = request.user
    logged_in_user = Profile.objects.get(user=user)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        if (first_name != "" and not first_name.isspace()):
            logged_in_user.first_name = first_name
        last_name = request.POST.get('last_name')
        if (last_name != "" and not last_name.isspace()):
            logged_in_user.last_name = last_name
        email = request.POST.get('email')
        if (email != "" and not email.isspace()):
            logged_in_user.email = email
        phone_number = request.POST.get('phone_number')
        if (phone_number != "" and not phone_number.isspace()):
            logged_in_user.phone_number = phone_number
        domicile = request.POST.get('domicile')
        if (domicile != "" and not domicile.isspace()):
            logged_in_user.domicile = domicile

        logged_in_user.save()
        return HttpResponseRedirect(reverse('user_info'))

    context = {'form': form}
    return render(request, "user.html", context)

def logout_user(request):
    logout(request)
    return redirect('user:login')