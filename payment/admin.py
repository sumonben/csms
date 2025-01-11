from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('class_roll','name','group','session','department','email','phone', 'card_no', 'amount', 'tran_id','tran_purpose','status', 'created_at',)
    list_filter = ('group','session','department','status', 'created_at','tran_purpose')
    search_fields = ('currency', 'status')

admin.site.register(PaymentGateway)

@admin.register(PaymentPurpose)
class UserAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title','title_en']
    filter_fields=[  'id','title',]

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title','title_en']
    filter_fields=[  'id','title','title_en']
