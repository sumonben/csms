from django.contrib import admin
from django.urls import path,include, re_path
import static
from . import views
from student import views as  view
from django.conf import settings
from django.conf.urls.static import static
from django import views as django_views

urlpatterns = [
    
    path('login/',views.admissionLogin, name='admission_login'),
    path('admission_form/', views.admissionForm, name="admission_form"),
    path('admission_form_submit/', views.admissionFormSubmit, name="admission_form_submit"),
    path('form_download/', views.formDownload, name='form_download'),
    path('search_admission_form/', views.SearchAdmissionView.as_view(), name='search_admission_form'),
    path('get_student_id_card/', views.IDCardView.as_view(), name='get_student_id_card'),
    path('', views.SubprocessesView, name='get_district'),

    path('jsi18n/', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),






]