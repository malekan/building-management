from django.conf.urls import url
from . import views

app_name = 'management'

urlpatterns = [
    url(r'^$', views.index)
]
