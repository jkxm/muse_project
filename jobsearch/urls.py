from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^api_to_db/$', views.api_to_db),
    # url(r'^index/$', views.search),
    url('', views.search),
]
