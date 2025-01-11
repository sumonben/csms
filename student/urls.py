from django.contrib import admin
from django.urls import path,include, re_path
from . import views
from payment import views
urlpatterns = [
    
    
        path('', views.searchPayment, name='search_payment'),




]