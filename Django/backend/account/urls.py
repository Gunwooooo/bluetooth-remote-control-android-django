from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('login/', views.user_login),
    path('join/', views.user_join),
    path('info/',views.user_info),
    path('duplicateCheck/', views.user_duplicate_check),
    path('protectorInquire/', views.user_protector_inquire),
    path('modifyInfo/', views.user_modify_info),
]