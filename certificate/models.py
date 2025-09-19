from django.db import models
from student.models import Student,SubjectChoice,Session,Group,Department,StudentCategory,Class,Adress
from payment.models import Transaction
# Create your models here.
class CertificateType(models.Model):
    serial=models.IntegerField(default=10)
    name=models.CharField(max_length=250)
    name_en=models.CharField(max_length=250)
    amount=models.IntegerField(default=10)
    template=models.CharField(max_length=250,blank=True,null=True)
    image=models.ImageField(upload_to='media/',blank=True,null=True,)
    is_active=models.BooleanField(default=False)
    is_auto_sign=models.BooleanField(default=False)
    is_join_sign=models.BooleanField(default=False)
    class Meta:
        ordering = ['serial']
        verbose_name=" সনদের ধরণ"
        verbose_name_plural=" সনদের ধরণ"
    def __str__(self):
        return self.name+'('+self.name_en+')'

class Certificate(models.Model):
    serial=models.IntegerField(default=0)
    name=models.CharField(max_length=100)
    name_bangla=models.CharField(max_length=100,blank=True, null=True)
    student=models.ForeignKey(Student,blank=True,null=True,on_delete=models.CASCADE)
    email=models.EmailField(max_length=50,null=True)
    phone=models.CharField(max_length=11,null=True)
    father_name_eng=models.CharField(max_length=100)
    father_name_bangla=models.CharField(max_length=100,blank=True, null=True)
    mother_name_eng=models.CharField(max_length=100)
    mother_name_bangla=models.CharField(max_length=100,blank=True, null=True)
    student_category=models.ForeignKey(StudentCategory,blank=True,null=True,on_delete=models.SET_NULL)
    session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    department=models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    class_year=models.ForeignKey(Class,blank=True,null=True,on_delete=models.SET_NULL)
    section=models.CharField(max_length=25,null=True, blank=True,)
    class_roll=models.CharField(max_length=11,null=True, blank=True,)
    exam_roll=models.CharField(max_length=25,null=True, blank=True,)
    registration=models.CharField(max_length=25,null=True, blank=True,)
    cgpa=models.CharField(max_length=4,null=True, blank=True,)
    passing_year=models.CharField( max_length=25, blank=True,null=True)
    subjects=models.ForeignKey(SubjectChoice,null=True, blank=True,on_delete=models.SET_NULL)
    adress=models.ForeignKey(Adress,null=True, blank=True,on_delete=models.SET_NULL)
    certificate_type=models.ForeignKey(CertificateType,null=True, blank=True,on_delete=models.SET_NULL)
    transaction=models.ForeignKey(Transaction,blank=True,null=True,on_delete=models.SET_NULL)
    language=models.CharField(max_length=15,null=True, blank=True,)
    is_valid=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name +':'+ self.phone