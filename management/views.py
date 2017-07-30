from django.shortcuts import render


def index(request):
    return render(request, template_name='management/index.html')


def login(request):
    return render(request, template_name='management/login.html')


def signup(request):
    return render(request, template_name='management/signup.html')
