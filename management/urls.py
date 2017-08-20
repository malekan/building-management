from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^home/$', views.index, name='home'),
    url(r'^whatis/$', views.whatis, name='whatis'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/account-activation/(?P<uid_base_64>[0-9a-zA-Z_\-]+)/(?P<token>[0-9a-zA-Z]{1,13}-[0-9a-zA-Z]{1,20})/$',
        views.activate_account, name='account-activation'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^messaging/$', views.messaging, name='messaging'),
    url(r'^bulletin_board/$', views.messaging, name='bulletin_board'),
    url(r'^dashboard_user/$', TemplateView.as_view(template_name='management/dashboard_user.html')),
    url(r'^building/new/$', views.new_building, name='new_building'),
    url(r'^building/(?P<building_id>)[0-9]+/$', views.make_building_page, name='building_page'),
    url(r'^building/(?P<building_id>[0-9]+)/edit/', views.BuildingUpdate, name='update_building'),
    url(r'^building/management/', TemplateView.as_view(template_name="management/building_management.html")),
    url(r'^unit/new/$', views.new_unit, name='new_unit'),
    url(r'^building/facility/new', views.new_facility, name='new_facility'),
    url(r'^building/delete/(?P<building_id>[0-9]+)/$', views.delete_building, name="delete_building"),
    url(r'^cost/new/$', views.new_cost, name="new_cost")
]
