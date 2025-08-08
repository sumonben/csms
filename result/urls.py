from django.contrib import admin
from django.urls import path,include, re_path
from . import views

urlpatterns = [
    
    path('', views.searchResult, name='search_result'),
    path('create_result', views.createResult, name='create_result'),
    path('summery_result', views.SummeryResult, name='summery_result'),
    path('subject_wise_marks', views.SubjectWiseMarks, name='subject_wise_marks'),
    path('get_subject_wise_marks', views.GetSubjectWiseMarks, name='get_subject_wise_marks'),
    path('delete_result', views.deleteResult, name='delete_result'),
    path('create_position', views.CreatePosition, name='create_position'),
    path('highest_marks', views.CreateHighestMarks, name='highest_marks'),
    path('option_create_result', views.OptionCreateResult, name='option_create_result'),
    path('option_create_position', views.OptionCreatePosition, name='option_create_position'),
    path('option_delete_result', views.OptionDeleteResult, name='option_delete_result'),
    path('option_highest_marks', views.OptionHighestMarks, name='option_highest_marks'),
    path('get_result_summery', views.OptionSummeryResult, name='get_result_summery'),
    path('option_subject_wise_marks', views.OptionSubjectWiseMarks, name='option_subject_wise_marks'),






]