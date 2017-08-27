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
    url(r'^manager_account/$', views.manager_account, name='manager_account'),
    url(r'^payment_initial/$', views.payment_initial, name='payment_initial'),
    url(r'^payment_final/$', views.payment_final, name='payment_final'),
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^buildings/(?P<building_id>[0-9]+)/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^buildings/(?P<building_id>[0-9]+)/messaging/$', views.messaging, name='messaging'),
    ## temporary
     # url(r'^buildings/(?P<building_id>[0-9]+)/bills/$', views.bills, name='bills'),
    ## temporary
    url(r'^buildings/(?P<building_id>[0-9]+)/messaging/sent_messages/$', views.messaging_sent, name='messaging_sent'),
    url(r'^buildings/(?P<building_id>[0-9]+)/bulletin_board/$', views.bulletin_board, name='bulletin_board'),
    url(r'^buildings/(?P<building_id>[0-9]+)/bulletin_board/(?P<bulletin_id>[0-9]+)/delete/$',
        views.delete_bulletin, name='delete_bulletin'),
    # url(r'^buildings/(?P<building_id>[0-9]+)/facility_info/$', views.facility_info, name='facility_info'),
    # url(r'^dashboard_user/$', views.dashboard_user, name='dashboard_user'),
    url(r'^buildings/(?P<building_id>[0-9]+)/edit/', views.BuildingUpdate, name='update_building'),
    url(r'^buildings/(?P<building_id>[0-9]+)/units/$', views.building_units, name='building_units'),
    url(r'^buildings/(?P<building_id>[0-9]+)/units/(?P<unit_id>[0-9]+)/delete/$', views.delete_unit,
        name='delete_unit'),
    url(r'^buildings/(?P<building_id>[0-9]+)/facilities/$', views.facilities, name='facilities'),
    url(r'^buildings/(?P<building_id>[0-9]+)/facilities/(?P<facility_id>[0-9]+)/delete/$', views.delete_facility,
        name='delete_facility'),
    url(r'^buildings/(?P<building_id>[0-9]+)/facilities/(?P<facility_id>[0-9]+)/facility_info/$', views.facility_info,
        name='facility_info'),
    url(r'^buildings/(?P<building_id>[0-9]+)/delete/$', views.delete_building, name="delete_building"),
    url(r'^cost/new/$', views.new_cost, name="new_cost"),


    url(r'^user_account/$', views.user_account, name='user_account'),
    url(r'^my_units/$', views.user_units, name='user_units'),
    url(r'^my_units/(?P<unit_id>[0-9]+)/dashboard', views.dashboard_user, name='dashboard_user'),
    url(r'^my_units/(?P<unit_id>[0-9]+)/bills/$', views.bills, name='bills'),
]
