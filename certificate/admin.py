from django.contrib import admin
from .models import CertificateType, Certificate
from import_export.admin import ExportActionMixin,ImportExportMixin

# Register your models here.
@admin.register(Certificate)
class CertificateAdmin(ExportActionMixin,admin.ModelAdmin):
    search_fields=[  'id','email','phone',]
    list_display=[ 'id','name','email','phone','student_category','session','group','department','class_year','is_valid']
    list_display_links = ['id','name','email','phone',]
    list_filter=['session','group','class_year','is_valid']
@admin.register(CertificateType)
class CertificateTypeAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=['id','serial','name','template']
    list_display_links=['id','serial','name','template']