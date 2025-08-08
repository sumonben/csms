from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('class_roll','name','group','session','department','phone', 'amount','tran_purpose','status', 'created_at',)
    list_filter = ('group','session','department','status', 'created_at','tran_purpose')
    search_fields = ('class_roll','name', 'status')
    actions=['export_as_csv']
    def export_as_csv(self, request, queryset):
    
        meta = self.model._meta
        field_names = ['class_roll','name','group','session', 'amount','tran_purpose','tran_id',] 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        total_amount=0
        student_count=0
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
            student_count=student_count+1   
            if obj.amount:
                total_amount=total_amount+obj.amount 
        writer.writerow(['Total amount = ', total_amount,"Number of student=",student_count])
        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display=[ 'gateway_name','store_id', 'store_pass', 'is_sandbox', 'is_active']
    filter_fields=['is_active',]
@admin.register(PaymentPurpose)
class UserAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title','title_en']
    filter_fields=[  'id','title',]

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title','title_en']
    filter_fields=[  'id','title','title_en']
@admin.register(PaymentConsession)
class PaymentConsessionAdmin(admin.ModelAdmin):
    list_display = ['class_roll','name','group','session','department',]
    filter_fields=[  'class_roll',]

