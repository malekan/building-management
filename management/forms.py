from django import forms
from .models import Building


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'number_of_floors', 'number_of_elevators')
