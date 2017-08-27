from django import forms
from .models import Building, Unit, Facility, Profile, Cost, Bulletin, Message


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'number_of_floors', 'number_of_elevators', 'main_pic', 'balance')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "نام"
        self.fields['address'].label = "آدرس"
        self.fields['description'].label = "توضیح"
        self.fields['number_of_floors'].label = "تعداد طبقات"
        self.fields['number_of_elevators'].label = "تعداد آسانسورها"
        self.fields['balance'].label = "موجودی اولیه"
        self.fields['main_pic'].label = "انتخاب تصویر"


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('unit_type', 'unit_number', 'story', 'area', 'number_of_bedrooms', 'number_of_parking_spaces',
                  'number_of_storage_rooms', 'options', 'description', 'owner', 'main_pic')

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['unit_type'].label = "نوع واحد"
        self.fields['unit_number'].label = "شماره‌ی واحد"
        self.fields['story'].label = "طبقه"
        self.fields['area'].label = "مساحت"
        self.fields['number_of_bedrooms'].label = "تعداد اتاق خواب"
        self.fields['number_of_parking_spaces'].label = "تعداد پارکینگ"
        self.fields['number_of_storage_rooms'].label = "تعداد انباری"
        self.fields['options'].label = "امکانات"
        self.fields['description'].label = "توضیح"
        self.fields['owner'].label = "مالک"
        self.fields['main_pic'].label = "انتخاب تصویر"


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'description', 'cost_per_hour')

    def __init__(self, *args, **kwargs):
        super(FacilityForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "نام"
        self.fields['description'].label = "توضیحات"
        self.fields['cost_per_hour'].label = "نرخ اجاره به ازای هر نیم ساعت"


class CostForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('number_of_unit', 'تعداد واحد'),
        ('number_of_people', 'تعداد نفر'),
        ('area', 'مساحت'),
    )
    building_id = forms.IntegerField(label="", widget=forms.HiddenInput(), required=True)
    should_be_billed = forms.BooleanField(label="برای این هزینه قبض صادر شود؟", required=False)
    bill_type = forms.CharField(label="صدور قبض براساس", widget=forms.Select(choices=TYPE_CHOICES), required=True)

    class Meta:
        model = Cost
        fields = ('fee', 'description', 'building_id', 'should_be_billed', 'bill_type')

    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.fields['fee'].label = "مبلغ پرداختی"
        self.fields['description'].label = "توضیحات"


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ('title', 'text')

    def __init__(self, *args, **kwargs):
        super(BulletinForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "عنوان"
        self.fields['text'].label = "متن"

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('receiver', 'title', 'text')

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "عنوان"
        self.fields['receiver'].label = "گیرنده"
        self.fields['text'].label = "متن پیام"
