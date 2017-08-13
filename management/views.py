from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User
from .models import Profile, Building, Unit
from .forms import BuildingForm, UnitForm, FacilityForm


def index(request):
    return render(request, template_name='management/index.html')


def login(request):
    return render(request, template_name='management/login.html')


def signup(request):
    if request.method == 'post':
        fullname = request.POST['fullname']
        signup_tel = request.POST['signup_tel']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pwd']
        avatar = request.POST['avatar']

        if User.objects.filter(username=username).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'username_error_message': 'این نام کابری قبلا استفاده شده است.'
            })
        if User.objects.filter(email=email).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'email_error_message': 'این ایمیل قبلا استفاده شده است.'
            })
        if Profile.objects.filter(mobile_number=signup_tel).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'tel_error_message': 'این شماره همراه قبلا استفاده شده‌ است.'
            })

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        profile = Profile(user=user, full_name=fullname, mobile_number=signup_tel, avatar=avatar)
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'management/dashboard.html')
        return render(request, template_name='management/signup.html')
    else:
        pass
    return render(request, template_name='management/signup.html')


# @login
def new_building(request):
    form = BuildingForm()
    return render(request, 'management/new_building_form.html', {'form': form})


class BuildingUpdate(UpdateView):
    form = BuildingForm
    context_object_name = 'form'
    template_name = 'management/update_building_form.html'


# @login
def new_unit(request):
    form = UnitForm()
    return render(request, 'management/new_unit_form.html', {'form': form})


# @login
def new_facility(request):
    form = FacilityForm()
    return render(request, 'management/new_facility_form', {'form': form})
