from django.contrib import admin
from django.urls import path,include, re_path
from . import views 
from payment import views as payment_views
from django import views as django_views

urlpatterns = [
    
        path('', views.frontPage, name='frontpage'),
        path('search_payment/', payment_views.searchPayment, name='search_payment'),
        path('jsi18n/', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),


]