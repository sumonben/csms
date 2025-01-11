from django.contrib import admin
from .models import StudentAdmission
from import_export.admin import ImportExportMixin
# Register your models here.
@admin.register(StudentAdmission)
class StudentAdmissionAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','name','student_details','ssc_roll','board','passing_year','quota','group','status']
    list_display_links = ['ssc_roll','name',]
    list_filter=['board','passing_year','quota','group',]
