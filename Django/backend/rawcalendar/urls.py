from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('modifyInfo/', views.rawcalendar_modify_info),
    path('info/', views.rawcalendar_info),
]
