from django.contrib import admin
from import_export.admin import ExportActionMixin,ImportExportMixin
from .models import Attendance, DailyAttendance

@admin.register(Attendance)
class StudentAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields=['class_roll']
    list_display=[ 'date','time','class_roll','name','group','session','student_category','department']
    list_display_links = ['name','class_roll']
    list_filter=['date','department','student_category','session','group']

@admin.register(DailyAttendance)
class DailyAttendanceAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields=['date',]
    list_display=[ 'date','science','humanities','business_studies','all','session']
    list_display_links = ['date','session']
    list_filter=['date','session',]

