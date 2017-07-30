from django.shortcuts import render
from .forms import BuildingForm, UnitForm


def index(request):
    return render(request, template_name='management/index.html')


def login(request):
    return render(request, template_name='management/login.html')


def signup(request):
    return render(request, template_name='management/signup.html')


def new_building(request):
    form = BuildingForm()
    return render(request, 'management/new_building_form.html', {'form': form})


def new_unit(request):
    form = UnitForm()
    return render(request, 'management/new_unit_form.html', {'form': form})
