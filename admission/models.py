from django.db import models
from student.models import Student,Subject,Session,StudentCategory, Department
from django.urls import reverse
from django.utils.html import format_html
from django.template.defaultfilters import escape

# Create your models here.

class StudentAdmission(models.Model):
    serial=models.IntegerField(default=10)
    student=models.OneToOneField(Student,blank=True,null=True,on_delete=models.SET_NULL)
    ssc_roll=models.CharField(max_length=25,blank=True,null=True)
    name=models.CharField(max_length=125,blank=True,null=True)
    passing_year=models.CharField( max_length=25, blank=True,null=True)
    board=models.CharField(max_length=25,blank=True,null=True)
    group=models.CharField(max_length=25,blank=True,null=True)
    admission_group=models.CharField(max_length=25,blank=True,null=True)
    admission_session=models.ForeignKey(Session,blank=True,null=True,on_delete=models.SET_NULL)
    student_category=models.ForeignKey(StudentCategory,blank=True,null=True,on_delete=models.SET_NULL)
    department=models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    quota=models.CharField(max_length=25,blank=True,null=True)
    status=models.CharField(max_length=100,default="Not Admitted")

    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.ssc_roll
    def student_details(self):
        stud=self.student
        if stud:
            return format_html('<a href="%s" target="_blank">%s</a>' % (reverse("admin:student_student_change", args=(stud.id,)) , escape(self.name+",\nRoll:"+stud.class_roll+', Phone:'+stud.phone)))
    student_details.allow_tags = True
    def save(self, *args, **kwargs):
           super().save(*args, **kwargs)
           if self.serial == None:
                self.serial = self.id
                super().save()
    


