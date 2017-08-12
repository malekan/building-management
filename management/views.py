from django.shortcuts import render
from .forms import BuildingForm, UnitForm, FacilityForm


def index(request):
    return render(request, template_name='management/index.html')


def login(request):
    return render(request, template_name='management/login.html')


def signup(request):
    if request.method == 'post':
        pass
    else:
        pass
    return render(request, template_name='management/signup.html')


# @login
def new_building(request):
    form = BuildingForm()
    return render(request, 'management/new_building_form.html', {'form': form})


# @login
def new_unit(request):
    form = UnitForm()
    return render(request, 'management/new_unit_form.html', {'form': form})


# @login
def new_facility(request):
    form = FacilityForm()
    return render(request, 'management/new_facility_form', {'form': form})
