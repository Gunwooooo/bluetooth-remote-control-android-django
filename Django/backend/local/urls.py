from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('hospital/', views.local_hospital),
    path('pharmacy/', views.local_pharmacy)
]
