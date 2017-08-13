from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'management'

urlpatterns = [
    url(r'home/$', views.index, name='home'),
    url(r'login/$', views.login_user, name='login'),
    url(r'signup/$', views.signup, name='signup'),
    url(r'^dashboard/$', TemplateView.as_view(template_name='management/dashboard.html')),
    url(r'^email/$', TemplateView.as_view(template_name='management/email.html')),
    url(r'building/new/$', views.new_building, name='new_building'),
    url(r'building/(?P<building_id>[0-9]+)/edit/', views.BuildingUpdate.as_view(), name='update_building'),
    url(r'unit/new/$', views.new_unit, name='new_unit'),
    url(r'building/facility/new', views.new_facility, name='new_facility'),
]
