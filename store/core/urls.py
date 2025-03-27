
from django.contrib import admin
from django.urls import path, include,re_path
from . import views

app_name = 'core'

urlpatterns = [
    path('helloworld/', views.HelloworldView.as_view(),name='hello_world'), #core:hello_world
    path('products/',views.ListProductsView.as_view(),name='products'),
]