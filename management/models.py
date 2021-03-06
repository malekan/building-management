import datetime
from django.utils import timezone
from . import jdate

import math

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# max lengths
names_length = 60
address_length = 300
short_description_length = 500
long_description_length = 1000


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=names_length)
    mobile_number = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    is_manager = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name + ' ' + self.mobile_number


class Building(models.Model):
    name = models.CharField(max_length=names_length)
    address = models.CharField(max_length=address_length)
    description = models.TextField(max_length=long_description_length)
    number_of_floors = models.IntegerField()
    number_of_elevators = models.IntegerField()
    # main_pic_src = models.CharField(max_length=5000, null=True, blank=True)
    main_pic = models.FileField(upload_to='building_images', default='../static/building_default.png')
    balance = models.IntegerField(default=0)
    manager = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    end_of_subscription = models.DateTimeField(null=True)


class Unit(models.Model):
    # types
    RESIDENTIAL = 'R'
    BUSINESS = 'B'
    TYPE_CHOICES = (
        (RESIDENTIAL, 'مسکونی'),
        (BUSINESS, 'تجاری'),
    )
    unit_type = models.CharField(max_length=1,
                                 choices=TYPE_CHOICES,
                                 default=RESIDENTIAL)
    unit_number = models.PositiveIntegerField()
    story = models.IntegerField()
    area = models.PositiveIntegerField()  # unit: m^2
    number_of_bedrooms = models.PositiveIntegerField(default=1)
    number_of_parking_spaces = models.PositiveIntegerField(default=1)
    number_of_storage_rooms = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    options = models.CharField(max_length=short_description_length, blank=True, null=True)
    main_pic = models.FileField(upload_to='unit_images', default='../../../static/unit_default.png')

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='owned_units')
    number_of_residents = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=2)
    ownership_info = models.TextField(max_length=long_description_length, blank=True, null=True)
    rental_status = models.BooleanField(default=False)
    tenant = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='rented_units')


class Pictures(models.Model):
    image = models.ImageField(upload_to='media/building_and_unit_pics')

    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)


class Bill(models.Model):
    # todo: types? types should be determined
    description = models.TextField(max_length=short_description_length)
    fee = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    due_date_time = models.DateTimeField()
    is_paid = models.BooleanField(default=False)


class Facility(models.Model):
    name = models.CharField(max_length=names_length)
    description = models.TextField(max_length=long_description_length)
    main_pic = models.FileField(upload_to='unit_images', default='../../../static/facility_default.png')
    cost_per_hour = models.PositiveIntegerField()

    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class OneHourReserve(models.Model):
    hour_number = models.PositiveIntegerField(validators=[MaxValueValidator(23)])
    reservation_status = models.PositiveIntegerField(validators=[MaxValueValidator(2)], default=0)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)


class FacilityReservation(models.Model):
    reservee = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # todo: confirmation status may not be necessary
    confirmation_status = models.BooleanField(default=False)
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True)


# todo: may not be needed at all
class Janitor(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    duty = models.CharField(max_length=names_length)
    contract_info = models.TextField(max_length=long_description_length)


# todo: should be taken care of later
class Cost(models.Model):
    date = models.DateTimeField()
    fee = models.IntegerField()
    description = models.TextField(max_length=short_description_length)

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def bill_based_on_area(self):
        units = self.building.unit_set.all()
        area_sum = units.aggregate(Sum('area'))['area__sum']
        for unit in units:
            fee = math.floor(self.fee * unit.area / area_sum)
            bill = Bill(description=self.description, fee=fee,
                        due_date_time=timezone.now() + datetime.timedelta(weeks=1),
                        unit=unit)
            bill.save()

    def bill_based_on_unit(self):
        units = self.building.unit_set.all()
        number_of_units = units.count()
        for unit in units:
            fee = math.floor(self.fee / number_of_units)
            bill = Bill(description=self.description, fee=fee,
                        due_date_time=timezone.now() + datetime.timedelta(weeks=1),
                        unit=unit)
            bill.save()

    def bill_based_on_number_of_residents(self):
        units = self.building.unit_set.all()
        residents_sum = units.aggregate(Sum('number_of_residents'))['number_of_residents__sum']
        for unit in units:
            fee = math.floor(self.fee * unit.number_of_residents / residents_sum)
            bill = Bill(description=self.description, fee=fee,
                        due_date_time=timezone.now() + datetime.timedelta(weeks=1),
                        unit=unit)
            bill.save()


class Bulletin(models.Model):
    title = models.CharField(max_length=2 * names_length)
    text = models.TextField(max_length=3 * long_description_length)
    date_time = models.DateTimeField()

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    @property
    def jalali_date(self):
        dt = self.date_time
        jd = jdate.gregorian_to_jd(dt.year, dt.month, dt.day)
        jalalidate = jdate.jd_to_persian(jd)
        return '' + str(math.floor(jalalidate[0])) + '/' + str(math.floor(jalalidate[1])) + '/' + \
               str(math.floor(jalalidate[2]))

    @property
    def jalali_time(self):
        return '' + str(self.date_time.hour) + ':' + str(self.date_time.minute)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='received_messages')
    date_time = models.DateTimeField()
    title = models.CharField(max_length=2 * names_length)
    text = models.TextField(max_length=3 * long_description_length)
    # confirmation status may not be needed
