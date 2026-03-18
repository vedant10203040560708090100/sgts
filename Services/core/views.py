from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    return render(request, 'core/login.html')

def contact(request):
    return render(request, 'core/contact.html')