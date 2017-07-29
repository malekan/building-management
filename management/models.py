import datetime
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# max lengths
names_length = 60
address_length = 300
short_description_length = 500
long_description_length = 1000


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=names_length)
    mobile_number = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='media/avatars')


class Building(models.Model):
    name = models.CharField(max_length=names_length)
    address = models.CharField(max_length=address_length)
    description = models.TextField(max_length=long_description_length)
    number_of_floors = models.IntegerField()
    number_of_elevators = models.IntegerField()

    manager = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    end_of_subscription = models.DateTimeField(null=True)


class Unit(models.Model):
    # types
    RESIDENTIAL = 'R'
    BUSINESS = 'B'
    TYPE_CHOICES = (
        (RESIDENTIAL, 'Residential'),
        (BUSINESS, 'Business'),
    )
    unit_type = models.CharField(max_length=1,
                                 choices=TYPE_CHOICES,
                                 default=RESIDENTIAL)

    area = models.IntegerField()  # unit: m^2
    number_of_bedrooms = models.IntegerField(default=1)
    number_of_parking_spaces = models.IntegerField(default=1)
    number_of_storage_rooms = models.IntegerField(default=1)
    description = models.TextField()

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='units')
    ownership_info = models.TextField(max_length=long_description_length, blank=True)
    rental_status = models.BooleanField(default=False)
    tenant = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


class Pictures(models.Model):
    image = models.ImageField(upload_to='media/building_and_unit_pics')

    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)


class Facility(models.Model):
    name = models.CharField(max_length=names_length)
    description = models.TextField(max_length=long_description_length)

    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class Bill(models.Model):
    # todo: types? types should be determined
    description = models.TextField(max_length=short_description_length)
    fee = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    due_date_time = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(weeks=1))
    is_paid = models.BooleanField(default=False)


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


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='messages')
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField()
    title = models.CharField(max_length=2 * names_length)
    text = models.TextField(max_length=3 * long_description_length)
    # confirmation status may not be needed
