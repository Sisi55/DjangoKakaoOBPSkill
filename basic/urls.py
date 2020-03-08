from django.contrib import admin
from django.urls import path, include
from basic import views

urlpatterns = [
    path('', views.index),
    path('list/', views.list)
]
