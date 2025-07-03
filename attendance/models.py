from django.db import models
from student.models import Student,Session,Group,StudentCategory,Department

# Create your models here.
class Attendance(models.Model):
    date=models.DateField(auto_now_add=True, null=True)
    time=models.TimeField(auto_now=True) 
    name=models.CharField(max_length=100,blank=True, null=True,verbose_name="Name In English:")
    class_roll=models.CharField(max_length=11,null=True, blank=True,)
    student=models.ForeignKey(Student,blank=True,null=True,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    student_category=models.ForeignKey(StudentCategory,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    section=models.CharField(max_length=25,null=True, blank=True,)
    department=models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    
class DailyAttendance(models.Model):
    date=models.DateField(auto_now_add=True, null=True)
    science=models.ImageField(default=0)
    humanities=models.ImageField(default=0)
    business_studies=models.ImageField(default=0)
    all=models.ImageField(default=0)
    session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    student_category=models.ForeignKey(StudentCategory,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    department=models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)