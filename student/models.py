from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import Field
from django.urls import reverse
from django.utils.html import format_html
from django.template.defaultfilters import escape
from import_export.resources import ModelResource
from smart_selects.db_fields import ChainedForeignKey
from datetime import datetime
import os


UserModel=get_user_model()
def rename_image(instance, filename):
        ext = filename.split('.')[-1]
        filename = str(instance.class_roll)+'.'+ext
        year=str(datetime.now().year)
        return os.path.join('media/student/'+year, filename)
# Create your models here.
class Group(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=100,unique=True)
    title_en=models.CharField(max_length=100,unique=True,blank=True,null=True)

    class Meta:
        ordering = ['serial']
    def __str__(self):
        return self.title_en


class StudentCategory(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=100,unique=True)
    title_en=models.CharField(max_length=100,unique=True,blank=True,null=True)

    class Meta:
        ordering = ['serial']
    def __str__(self):
        return self.title
    
class Department(models.Model):
    serial=models.IntegerField(default=10)
    name=models.CharField(max_length=100,unique=True)
    name_en=models.CharField(max_length=100,null=True,blank=True,verbose_name="Name(In English)")
    code=models.CharField(max_length=20, null=True,blank=True)
    about=RichTextUploadingField(blank=True,null=True)
    about_en=RichTextUploadingField(blank=True,null=True,verbose_name="About(In English)")
    professor=models.IntegerField(default=0)
    associate_professor=models.IntegerField(default=0)
    assistant_professor=models.IntegerField(default=0)
    lecturer=models.IntegerField(default=0)
    demonstrator=models.IntegerField(default=0)
    
    class Meta:
        ordering = ['serial']
    def __str__(self):
        return self.name_en


class Branch(models.Model):
    serial=models.IntegerField(default=10)
    code=models.CharField(max_length=20, null=True,blank=True)
    name=models.CharField(max_length=100,unique=True)
    name_en=models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        ordering = ['serial']
    
    def __str__(self):
        return self.name

class Session(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=100,unique=True)
    title_en=models.CharField(max_length=100,unique=True,blank=True,null=True)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.title_en
    
    
class Class(models.Model):
    serial=models.IntegerField(default=10)
    title=models.CharField(max_length=100,unique=True)
    title_en=models.CharField(max_length=100,unique=True,blank=True,null=True)

    class Meta:
        ordering = ['serial']
    def __str__(self):
        return self.title
    

  
class Subject(models.Model):
    serial=models.IntegerField(default=10)
    name=models.CharField(max_length=100,null=True,blank=True)
    name_en=models.CharField(max_length=100,null=True,blank=True)
    code=models.CharField(max_length=20, null=True,blank=True)
    group=models.ManyToManyField(Group, blank=True,)
    department=models.ManyToManyField(Department, blank=True,)
    type=models.CharField(max_length=25,blank=True,null=True)
    is_practical=models.BooleanField(default=False)
    is_available=models.BooleanField(default=True)



    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.name_en:
            return self.name_en
        else:
            return '1'

class TestSubject(models.Model):
    serial=models.IntegerField(default=10)
    name=models.CharField(max_length=100,null=True,blank=True)
    name_en=models.CharField(max_length=100,null=True,blank=True)
    code=models.CharField(max_length=20, null=True,blank=True)
    group=models.ManyToManyField(Group, blank=True,)
    department=models.ManyToManyField(Department, blank=True,)
    type=models.CharField(max_length=25,blank=True,null=True)
    is_available=models.BooleanField(default=True)



    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.name_en:
            return self.name_en
        else:
            return '1'
 
class Division(models.Model):
    name=models.CharField(max_length=25,unique=True)
    name_en=models.CharField(max_length=15,unique=True)
    link=models.CharField(max_length=15,null=True,blank=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name_en

class District(models.Model):
    name=models.CharField(max_length=25,unique=True)
    name_en=models.CharField(max_length=25,unique=True)
    lattitude=models.CharField(max_length=15,blank=True,null=True)
    longitude=models.CharField(max_length=15, blank=True,null=True)
    division=ChainedForeignKey(Division, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=15,null=True,blank=True)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name_en

class Upazilla(models.Model):
    name=models.CharField(max_length=25)
    name_en=models.CharField(max_length=25)
    district=models.ForeignKey(District, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=15,null=True,blank=True)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name_en

class Union(models.Model):
    name=models.CharField(max_length=25)
    name_en=models.CharField(max_length=25)
    upazilla=models.ForeignKey(Upazilla, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=15,null=True,blank=True)

    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name_en

class GuardianInfo(models.Model):
    serial=models.IntegerField(default=10)
    father_name=models.CharField(max_length=100,blank=True,null=True)
    father_name_en=models.CharField(max_length=100,blank=True,null=True)
    profession_of_father=models.CharField(max_length=25,blank=True,null=True)
    father_nid=models.CharField(max_length=25,blank=True,null=True)
    mother_name=models.CharField(max_length=100,blank=True,null=True)
    mother_name_en=models.CharField(max_length=100,blank=True,null=True)
    profession_of_mother=models.CharField(max_length=25,blank=True,null=True)
    mother_nid=models.CharField(max_length=100,blank=True,null=True)
    guardian_phone=models.CharField(max_length=11,blank=True,null=True)
    anual_income=models.CharField(max_length=11,blank=True,null=True)
    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.father_name:
            return self.father_name
        else:
            return '1'
    
class Adress(models.Model):
    serial=models.IntegerField(default=10)
    village_or_house=models.CharField(max_length=50,blank=True,null=True)
    house_or_street_no=models.CharField(max_length=25,blank=True,null=True)
    post_office=models.CharField(max_length=25,blank=True,null=True)
    division=models.ForeignKey(Division,blank=True,null=True,on_delete=models.SET_NULL)
    district=models.ForeignKey(District,blank=True,null=True,on_delete=models.SET_NULL)
    upazilla=models.ForeignKey(Upazilla,blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.village_or_house:
            return self.village_or_house
        else:
            return '1'
            
class Student(models.Model):
    std_id=models.IntegerField(default=10)
    name=models.CharField(max_length=100,blank=True, null=True,verbose_name="Name In English:")
    name_bangla=models.CharField(max_length=100,blank=True, null=True)
    email=models.EmailField(max_length=50,blank=True, null=True)
    phone=models.CharField(max_length=11,blank=True, null=True)
    class_roll=models.CharField(max_length=11,null=True, blank=True,)
    session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    student_category=models.ForeignKey(StudentCategory,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    section=models.CharField(max_length=25,null=True, blank=True,)
    department=models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    exam_roll=models.CharField(max_length=25,null=True, blank=True,)
    registration=models.CharField(max_length=25,null=True, blank=True,)
    class_year=models.ForeignKey(Class,blank=True,null=True,on_delete=models.SET_NULL)
    cgpa=models.CharField(max_length=15,null=True, blank=True,)
    date_of_birth=models.DateField(blank=True, null=True)
    gender=models.CharField(max_length=15,null=True, blank=True,)
    passing_year=models.CharField( max_length=25, blank=True,null=True)
    nationality=models.CharField(max_length=15,null=True, blank=True,)
    birth_registration=models.CharField(max_length=25,null=True, blank=True,)
    religion=models.CharField(max_length=15,null=True, blank=True,)
    blood_group=models.CharField(max_length=10,null=True, blank=True,)
    marital_status=models.CharField(max_length=25,null=True, blank=True,)
    guardian_info=models.ForeignKey(GuardianInfo,on_delete=models.SET_NULL,null=True, blank=True,)
    present_adress=models.ForeignKey(Adress,null=True, blank=True,related_name="present_adress",on_delete=models.SET_NULL)
    permanent_adress=models.ForeignKey(Adress,null=True, blank=True,related_name="permanent_adress",on_delete=models.SET_NULL)
    image=models.ImageField(upload_to=rename_image,blank=True,null=True) 
    signature=models.ImageField(upload_to='media/student/%Y',blank=True,null=True)
    user=models.OneToOneField(UserModel,blank=True,null=True,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    fourth_subject=models.ForeignKey(Subject,blank=True,null=True,on_delete=models.SET_NULL)


    def user_link(self):
        if self.user is not None:
            return format_html('<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user.username)))
        else:
            return None
    user_link.allow_tags = True
    user_link.short_description = "User"
    
    def __str__(self):
        if self.phone:
            return self.name +':'+ self.phone
        else:
            return self.name +':'+ self.class_roll

    
    def __unicode__(self):
        return self.name_bangla
    def delete(self, *args, **kwargs):
        if bool(self.image) == True :
            os.remove(self.image.path)
        super(Student, self).delete(*args, **kwargs)
    
    
    
    
class SscEquvalent(models.Model):
    serial=models.IntegerField(default=10)
    student=models.ForeignKey(Student,blank=True,null=True,on_delete=models.CASCADE)
    ssc_or_equvalent=models.CharField(max_length=25,blank=True,null=True)
    ssc_board=models.CharField(max_length=25,blank=True,null=True)
    ssc_group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    ssc_session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    ssc_exam_roll=models.CharField(max_length=25,blank=True,null=True)
    ssc_regitration_no=models.CharField(max_length=25,blank=True,null=True)
    ssc_cgpa_with_4th=models.CharField(max_length=25,blank=True,null=True)
    ssc_cgpa_without_4th=models.CharField(max_length=25,blank=True,null=True)
    ssc_passing_year=models.CharField( max_length=25, blank=True,null=True)
    
    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.student:
            return self.student.name+': '+self.student.phone
        return '1'
    

class SubjectChoice(models.Model):
    serial=models.IntegerField(default=10)
    student=models.ForeignKey(Student,blank=True,null=True,on_delete=models.CASCADE)
    compulsory_subject=models.ManyToManyField(Subject,related_name='compulsory_subject',blank=True,)
    optional_subject=models.ManyToManyField(Subject,related_name='optional_subject',blank=True,)
    fourth_subject=models.ForeignKey(Subject,blank=True,null=True,on_delete=models.SET_NULL)

    
    class Meta:
        ordering = ['serial']
    def __str__(self):
        if self.student is not None:
            return self.student.name+': '+self.student.phone
        return '1'
  


class Choice(models.Model):
    class_roll=models.CharField(max_length=255)
    name=models.CharField(max_length=255,blank=True, null=True)
    subject1=models.ForeignKey(Subject,related_name='subject1',blank=True,null=True,on_delete=models.SET_NULL)
    subject2=models.ForeignKey(Subject,related_name='subject2',blank=True,null=True,on_delete=models.SET_NULL)
    subject3=models.ForeignKey(Subject,related_name='subject3',blank=True,null=True,on_delete=models.SET_NULL)
    subject4=models.ForeignKey(Subject,related_name='subject4',blank=True,null=True,on_delete=models.SET_NULL)
    subject5=models.ForeignKey(Subject,related_name='subject5',blank=True,null=True,on_delete=models.SET_NULL)
    subject6=models.ForeignKey(Subject,related_name='subject6',blank=True,null=True,on_delete=models.SET_NULL)
    fourth_subject=models.ForeignKey(Subject,blank=True,null=True,on_delete=models.SET_NULL)
    class Meta:
        ordering = ['id']
    def __str__(self):
        if self.class_roll is not None:
            return self.class_roll+': '+self.name
        return self.class_roll
