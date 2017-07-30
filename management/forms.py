from django import forms
from .models import Building, Unit


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'number_of_floors', 'number_of_elevators')


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('unit_type', 'area', 'number_of_bedrooms', 'number_of_parking_spaces',
                  'number_of_storage_rooms', 'description', 'owner')
