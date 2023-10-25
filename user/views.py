from django.shortcuts import render

def user_info(request):
    return render(request, "user.html")