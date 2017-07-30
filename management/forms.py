from django import forms
from .models import Building, Unit, Facility


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'number_of_floors', 'number_of_elevators')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "نام"
        self.fields['address'].label = "آدرس"
        self.fields['description'].label = "توضیح"
        self.fields['number_of_floors'].label = "تعداد طبقات"
        self.fields['number_of_elevators'].label = "تعداد آسانسورها"


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('unit_type', 'area', 'number_of_bedrooms', 'number_of_parking_spaces',
                  'number_of_storage_rooms', 'description', 'owner')

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['unit_type'].label = "نوع واحد"
        self.fields['area'].label = "آدرس"
        self.fields['description'].label = "توضیح"
        self.fields['number_of_floors'].label = "تعداد طبقات"
        self.fields['number_of_elevators'].label = "تعداد آسانسورها"


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'description', 'building')

    def __init__(self, *args, **kwargs):
        super(FacilityForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "نام"
        self.fields['description'].label = "توضیحات"
        self.fields['building'].label = "ساختمان"
