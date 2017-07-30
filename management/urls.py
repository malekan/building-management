from django.conf.urls import url
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^$', views.index),
    url(r'login/$', views.login),
    url(r'signup/$', views.signup),
    url(r'building/new/$', views.new_building)
]
