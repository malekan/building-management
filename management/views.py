import pytz
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.template import loader, Context
from django.http import JsonResponse
from django.utils import timezone
import datetime
import pytz

from django.contrib.auth.models import User
from .models import Profile, Building, Unit, Facility, Bulletin, OneHourReserve, Message
from .forms import BuildingForm, UnitForm, FacilityForm, CostForm, BulletinForm, MessageForm


def index(request):
    return render(request, template_name='management/index.html')


def whatis(request):
    return render(request, template_name='management/whatis.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        signup_tel = request.POST['signup_tel']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        # avatar = request.POST['avatar']

        if Profile.objects.filter(mobile_number=signup_tel).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'tel_error_message': 'این شماره همراه قبلا استفاده شده‌ است.'
            })
        if User.objects.filter(email=email).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'email_error_message': 'این ایمیل قبلا استفاده شده است.'
            })
        if User.objects.filter(username=username).count() == 1:
            return render(request, template_name='management/signup.html', context={
                'username_error_message': 'این نام کابری قبلا استفاده شده است.'
            })

        user = User(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        profile = Profile(user=user, full_name=fullname, mobile_number=signup_tel,
                          is_manager=True if user_type == 'manager' else False)
        profile.save()
        current_site = get_current_site(request)
        message_template = loader.get_template('management/account_activation_confirmation_email.html')
        context = {
            'fullname': profile.full_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        message = message_template.render(context)
        mail_subject = 'سیما: فعال‌سازی حساب کاربری'
        mail = EmailMessage(subject=mail_subject, body=message, to=[email])
        try:
            mail.send()
        except BadHeaderError:
            user.delete()
            return render(request, 'management/signup.html', {
                'email_error_message': 'ایمیل وارد شده معتبر نیست.'
            })
        return render(request, 'management/login.html', {
            'email_sent_message': 'ایمیل فعالسازی حساب کاربری برای شما ارسال شد.'
        })

    else:
        return render(request, template_name='management/signup.html')


def activate_account(request, uid_base_64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid_base_64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'حساب کاربری شما با موفقت فعال شد! اکنون می‌توانید وارد شوید.')
        return redirect(reverse('management:login'))


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_profile = get_object_or_404(Profile, user=user)
                if user_profile.is_manager:
                    return redirect(reverse('management:buildings'))
                else:
                    return redirect(reverse('management:user_units'))
            else:
                return render(request, 'management/login.html', {
                    'login_error_message': 'حساب کاربری شما غیرفعال است.'
                })
        else:
            return render(request, 'management/login.html', {
                'login_error_message': 'اطلاعات وارد شده صحیح نیست.'
            })
    return render(request, template_name='management/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('management:login'))


@login_required
def dashboard(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    return render(request, 'management/dashboard.html', {
        'building': building,
    })


@login_required
def dashboard_user(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return render(request, 'management/dashboard_user.html', {
        'unit': unit,
    })


@login_required
def buildings(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            building = form.save(commit=False)
            print(request.FILES)
            building.manager = get_object_or_404(Profile, user=request.user)
            building.save()
    form = BuildingForm()
    cost_form = CostForm()
    [manager] = list(Profile.objects.filter(user=request.user).all())
    building_list = Building.objects.filter(manager=manager)
    return render(request, 'management/building_management.html', {
        'new_building_form': form,
        'new_cost_form': cost_form,
        'building_list': building_list,
    })


@login_required
def building_units(request, building_id):
    if request.method == 'POST':
        form = UnitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            unit = form.save(commit=False)
            print(request.FILES)
            unit.building = get_object_or_404(Building, pk=building_id)
            unit.save()
    building = get_object_or_404(Building, pk=building_id)
    units_list = building.unit_set.all()
    new_unit_form = UnitForm()
    return render(request, 'management/building_units.html', {
        'building': building,
        'units_list': units_list,
        'new_unit_form': new_unit_form
    })


@login_required
def delete_unit(request, building_id, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    unit.delete()
    if get_object_or_404(Profile, user=request.user).is_manager:
        return redirect('/buildings/' + building_id + '/units/')
    else:
        return redirect('/my_units/')


def new_cost(request):
    if request.method == 'POST':
        form = CostForm(request.POST)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.building = get_object_or_404(Building, pk=form.cleaned_data['building_id'])
            cost.date = timezone.now()
            cost.save()
            cost.building.balance -= cost.fee
            if form.cleaned_data['should_be_billed']:
                bill_type = form.cleaned_data['bill_type']
                if bill_type == 'area':
                    cost.bill_based_on_area()
                elif bill_type == 'number_of_unit':
                    cost.bill_based_on_unit()
                else:
                    cost.bill_based_on_number_of_residents()
    return redirect(reverse('management:buildings'))


@login_required
def delete_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    building.delete()
    return redirect(reverse('management:buildings'))


@login_required
class BuildingUpdate(UpdateView):
    form = BuildingForm
    context_object_name = 'update_form'
    template_name = 'management/building_management.html'


@login_required
def facilities(request, building_id):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.building = get_object_or_404(Building, pk=building_id)
            facility.save()
            for i in range(24):
                one_hour = OneHourReserve(hour_number=i, facility=facility)
                one_hour.save()

    building = get_object_or_404(Building, pk=building_id)
    facility_list = building.facility_set.all()
    form = FacilityForm()
    return render(request, 'management/facilities.html', {
        'building': building,
        'facility_list': facility_list,
        'new_facility_form': form,
    })


@login_required
def delete_facility(request, building_id, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    facility.delete()
    return redirect('/buildings/' + building_id + '/facilities/')


@login_required
def facility_info(request, building_id, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    return render(request, 'management/facility_info.html', {
        'building': facility.building,
        'facility': facility,
        'n': range(12),
    })


@login_required
def messaging(request, building_id):
    if request.method == 'POST':
        new_message(request)
    building = get_object_or_404(Building, pk=building_id)
    receiver = get_object_or_404(Profile, user=request.user)
    inbox_messages = Message.objects.filter(receiver=receiver).all()
    message_form = MessageForm()
    return render(request, 'management/messaging.html', {
        'building': building,
        'message_form': message_form,
        'inbox_list': inbox_messages
    })


def new_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = get_object_or_404(Profile, user=request.user)
            msg.date_time = timezone.now()
            msg.save()


@login_required
def bills(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return render(request, 'management/bills.html', {
        'unit_bills': unit.bill_set.all(),
    })


@login_required
def messaging_sent(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    sender = get_object_or_404(Profile, user=request.user)
    sent_messages = Message.objects.filter(sender=sender).all()
    return render(request, 'management/messaging_sent.html', {
        'building': building,
        'sent_list': sent_messages
    })


@login_required
def bulletin_board(request, building_id):
    if request.is_ajax():
        bulletin_id = request.GET['bulletin_id']
        bulletin = get_object_or_404(Bulletin, pk=bulletin_id)
        data = {
            'bulletin_title': bulletin.title,
            'bulletin_text': bulletin.text,
        }
        return JsonResponse(data)
    if request.method == 'POST':
        form = BulletinForm(request.POST)
        if form.is_valid():
            bulletin = form.save(commit=False)
            bulletin.date_time = timezone.now()
            bulletin.building = get_object_or_404(Building, pk=building_id)
            bulletin.save()
    building = get_object_or_404(Building, pk=building_id)
    bulletins_list = building.bulletin_set.order_by('-date_time')
    new_bulletin_form = BulletinForm()
    return render(request, 'management/bulletin_board.html', {
        'building': building,
        'bulletins_list': bulletins_list,
        'new_bulletin_form': new_bulletin_form,
    })


@login_required
def delete_bulletin(request, building_id, bulletin_id):
    bulletin = get_object_or_404(Bulletin, pk=bulletin_id)
    bulletin.delete()
    return redirect('/buildings/' + building_id + '/bulletin_board/')


# @login_required
# def facility_info(request, facility_id):
#     facility = get_object_or_404(Facility, pk=facility_id)
#     return render(request, 'management/facility_info.html', {
#         'facility': facility,
#     })



@login_required
def manager_account(request):
    return render(request, 'management/manager_account.html')


@login_required
def user_account(request):
    return render(request, 'management/user_account.html')


@login_required
def payment_initial(request):
    return render(request, 'management/payment_initial.html')


@login_required
def payment_final(request):
    messages.add_message(request, messages.INFO, 1)
    return render(request, 'management/payment_final.html')


# ######################################## resident ############
@login_required
def user_units(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    unit_list = Unit.objects.filter(owner=user_profile)
    return render(request, 'management/resident_units.html', {
        'unit_list': unit_list,
    })
