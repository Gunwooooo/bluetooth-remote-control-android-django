from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from . import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('user/join/', views.user_join),
    path('user/info/', views.user_info),
    path('user/login/', views.user_login),
    path('user/allchat/', views.allChat),
    path('user/chatting/', views.entChat),
    path('user/chatting/all/', views.chatting),
    path('video/', views.video),
    path('board/', views.board),
    path('board/card/', views.card),
    path('add_card/', views.add_card),
    path('introduction/', views.introduction),
    path('my_question/', views.my_qustion),
    path('select_question/', views.select_question),
    path('interview/', views.interview),
    path('recommend/', views.recommend),
    path('title/', views.title),
    path('analyze/', views.analyze),
    path('wordcloud/', views.wordcloud),
    path('mylist/', views.mylist),
    path('daily/', views.daily),
    path('count/', views.count),
    path('result/', views.result),
    path('result/all/', views.resultall),
    path('user/profile/', views.profile),
]