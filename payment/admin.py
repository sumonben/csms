from django.contrib import admin
from django.http import HttpResponse
# Register your models here.
from django.contrib import admin
from .models import *
import csv
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('class_roll','name','group','session','department','email','phone', 'card_no', 'amount', 'tran_id','tran_purpose','status', 'created_at',)
    list_filter = ('group','session','department','status', 'created_at','tran_purpose')
    search_fields = ('currency', 'status')
    actions = ("export_as_csv",)
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        header = field_names + ['calculated_column']
        writer.writerow(header)
        payment=0
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
            payment=payment+obj.amount 
        header = ['All Payment (BDT)'] + [payment]
        writer.writerow(header)
        return response

    export_as_csv.short_description = "Export Selected"
admin.site.register(PaymentGateway)

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
