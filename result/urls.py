from django.contrib import admin
from django.urls import path,include, re_path
from . import views

urlpatterns = [
    
    path('', views.searchResult, name='search_result'),
    path('create_result', views.createResult, name='create_result'),
    path('delete_result', views.deleteResult, name='delete_result'),
    path('create_position', views.CreatePosition, name='create_position'),
    path('option_create_result', views.OptionCreateResult, name='option_create_result'),
    path('option_create_position', views.OptionCreatePosition, name='option_create_position'),
    path('option_delete_result', views.OptionCreateResult, name='option_delete_result'),






]