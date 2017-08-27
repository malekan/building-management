from django.contrib import admin
from .models import Profile, Building, Unit, Facility, Cost, Bill, Message

admin.site.register(Profile)
admin.site.register(Building)
admin.site.register(Unit)
admin.site.register(Facility)
admin.site.register(Cost)
admin.site.register(Bill)
admin.site.register(Message)
