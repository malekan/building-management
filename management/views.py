from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User
from .models import Profile, Building, Unit
from .forms import BuildingForm, UnitForm, FacilityForm


def index(request):
    return render(request, template_name='management/index.html')

def whatis(request):
    return render(request, template_name='management/whatis.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'management/dashboard.html')
            else:
                return render(request, 'management/login.html', {
                    'login_error_message': 'حساب کاربری شما غیرفعال شده است.'
                })
        else:
            return render(request, 'management/login.html', {
                'login_error_message': 'اطلاعات وارد شده صحیح نیست.'
            })
    return render(request, template_name='management/login.html')


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'management/index.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        signup_tel = request.POST['signup_tel']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # avatar = request.POST['avatar']

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
        profile = Profile(user=user, full_name=fullname, mobile_number=signup_tel)
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'management/dashboard.html')

        return render(request, template_name='management/signup.html', context={
            'auth_error': 'با عرض پوزش خطایی رخ داده است. لطفا دوباره امتحان کنید.'
        })

    return render(request, template_name='management/signup.html')


@login_required
def new_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            # building.main_pic = request.FILES['main_pic']
            [building.manager] = list(Profile.objects.filter(user=request.user).all())
            building.save()
    form = BuildingForm()
    return render(request, 'management/building_management.html', {'new_building_form': form})


@login_required
def make_building_page(request, building_id):
    form = UnitForm()
    return render(request, 'management/building_page.html', context={
        'building_id': building_id,'new_unit_form': form

    })


@login_required
class BuildingUpdate(UpdateView):
    form = BuildingForm
    context_object_name = 'update_form'
    template_name = 'management/building_management.html'


@login_required
def new_unit(request):
    form = UnitForm()
    return render(request, 'management/building_page.html', {'new_unit_form': form})


@login_required
def new_facility(request):
    form = FacilityForm()
    return render(request, 'management/new_facility_form.html', {'form': form})
