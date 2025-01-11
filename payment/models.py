from django.db import models
from student.models import Group, Session,Department
# Create your models here.
class PaymentType(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=500, blank=True, null=True)
    title_en=models.CharField(max_length=500, blank=True, null=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['serial']
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Type"
    def __str__(self):
        return str(self.id)+": "+self.title 

class PaymentPurpose(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=500, blank=True, null=True)
    title_en=models.CharField(max_length=500, blank=True, null=True)
    subtitle=models.CharField(max_length=500, blank=True, null=True)
    subtitle_en=models.CharField(max_length=500, blank=True, null=True)
    cause=models.CharField(max_length=500, blank=True, null=True)
    cause_en=models.CharField(max_length=500, blank=True, null=True)
    start_date=models.DateTimeField(blank=True, null=True)
    end_date=models.DateTimeField(blank=True, null=True)
    payment_type=models.ForeignKey(PaymentType,blank=True,null=True,on_delete=models.SET_NULL)
    amount=models.IntegerField(default=10)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['serial']
        verbose_name = "Payment Purpose"
        verbose_name_plural = "Payment Purpose"
    def __str__(self):
        return self.title 


class Transaction(models.Model):
    class_roll = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    phone=models.CharField(max_length=11,blank=True,null=True,)
    email=models.EmailField(max_length=50,blank=True,null=True)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    department=models.ForeignKey(Department,blank=True,null=True,on_delete=models.SET_NULL)
    phone=models.CharField(max_length=11,blank=True,null=True,)
    email=models.EmailField(max_length=50,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_id = models.CharField(max_length=15,unique=True)
    tran_purpose=models.ForeignKey(PaymentPurpose,blank=True,null=True,on_delete=models.SET_NULL)
    val_id = models.CharField(max_length=75)
    card_type = models.CharField(max_length=150)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_no = models.CharField(max_length=55, null=True)
    bank_tran_id = models.CharField(max_length=155, null=True)
    status = models.CharField(max_length=55)
    tran_date = models.DateTimeField()
    currency = models.CharField(max_length=10)
    card_issuer = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=15)
    card_issuer_country = models.CharField(max_length=55)
    card_issuer_country_code = models.CharField(max_length=55)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    verify_sign = models.CharField(max_length=155)
    verify_sign_sha2 = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=15)
    risk_title = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.tran_id

        
class PaymentGateway(models.Model):

    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        verbose_name = "Payment Gateway"
        verbose_name_plural = "Payment Gateway"

