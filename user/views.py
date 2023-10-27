from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random


@login_required(login_url='/login')
def user_info(request):
    return render(request, "user.html")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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


def logout_user(request):
    logout(request)
    return redirect('user:login')
