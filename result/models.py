from django.db import models
from student.models import Subject,Group,TestSubject

# Create your models here.
class Exam(models.Model):
    serial=models.IntegerField(default=0)
    title=models.CharField(max_length=150,blank=True,null=True)
    title_en=models.CharField(max_length=150,blank=True,null=True)
    type=models.CharField(max_length=150,blank=True,null=True)
    is_practical_applicable=models.BooleanField(default=False)
    minimum_threshold=models.IntegerField(blank=True,null=True)
    is_active=models.BooleanField(default=False)

    
    class Meta:
        ordering = ['serial']
    def __str__(self):
        return self.title_en

class HighestMarks(models.Model):
    class_roll=models.CharField(max_length=25,blank=True,null=True)
    exam=models.ForeignKey(Exam,on_delete=models.SET_NULL,blank=True,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,blank=True, null=True)
    highest_mark=models.IntegerField(blank=True,null=True)
    class Meta:
        ordering = ['-subject','-highest_mark']
    def __str__(self):
        if self.class_roll is not None:
            return self.class_roll+': '+self.subject.name_en
        return self.class_roll
    
class Marks(models.Model):
    serial=models.IntegerField(default=0)
    class_roll=models.CharField(max_length=10,)
    name=models.CharField(max_length=100,blank=True, null=True)
    subject=models.ForeignKey(Subject,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)    
    exam=models.ForeignKey(Exam,blank=True,null=True,on_delete=models.SET_NULL)
    MCQ=models.IntegerField(blank=True,null=True)
    CQ=models.IntegerField(blank=True,null=True)
    practical=models.IntegerField(blank=True,null=True)
    total=models.IntegerField(blank=True,null=True)
    highest_mark=models.ForeignKey(HighestMarks,blank=True,null=True,on_delete=models.SET_NULL)
    grade=models.CharField(max_length=150,blank=True,null=True)
    cgpa=models.CharField(max_length=150,blank=True,null=True)
     
    class Meta:
        ordering = ['serial']
        unique_together=('class_roll','subject','exam')
    def __str__(self):
        if self.subject is not None:
            return self.class_roll+': '+self.subject.name_en
        return self.class_roll
    def subject_name(self):
        if self.subject is not None:
            return self.subject.name_en
    def before_save_instance(self, instance, using_transactions, dry_run):
        print(instance)
    def save(self, *args, **kwargs):
        total=0
        
        if self.subject:
            group=Group.objects.filter(id=3).first()
            subj=Subject.objects.filter(name_en=self.subject.name_en).first()

            if group in subj.group.all():
                if self.CQ:
                    total=total+self.CQ
                    if self.CQ<17:
                        self.grade="F"
                        self.cgpa=0
                else:
                    self.grade="Absent"
                    self.cgpa=None
                    
                if self.MCQ:
                    total=total+self.MCQ
                    if self.MCQ<8:
                        self.cgpa=0
                        self.grade="F"
                else:
                    self.grade="Absent"
                    self.cgpa=None
                
                if self.exam.is_practical_applicable:
                    print("practical")
                    total=total+self.practical
                    if self.practical<8:
                        self.cgpa=0
                        self.grade="F"
                else:
                    total=round(total*(100/75), 2)
            else:
                if self.subject.id==2:
                    if self.CQ:
                        total=total+self.CQ
                        if self.CQ<33:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                else:
                    if self.CQ:
                        total=total+self.CQ
                        if self.CQ<23:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    

                    if self.MCQ:
                        total=total+self.MCQ
                        if self.MCQ<10:
                            self.cgpa=0
                            self.grade="F"
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                        


            self.total=total

            if self.grade == 'F':
                self.cgpa=0
            elif self.grade == 'Absent':
                self.cgpa=None
            else: 
                if total<33:
                    self.cgpa=0
                    self.grade="F"

                elif total>=33 and total<40:
                    self.cgpa=1
                    self.grade="D"

                elif total>=40 and total<50:
                    self.cgpa=2
                    self.grade="C"
                elif total>=50 and total<60:
                    self.cgpa=3
                    self.grade="B"
                elif total>=60 and total<70:
                    self.cgpa=3.5
                    self.grade="A-"
                elif total>=70 and total<80:
                    self.cgpa=4
                    self.grade="A"
                else:
                    self.cgpa=5
                    self.grade="A+"



        super(Marks, self).save(*args, **kwargs)

class TestMarks(models.Model):
    class_roll=models.CharField(max_length=10,)
    name=models.CharField(max_length=100,blank=True, null=True)
    subject=models.ForeignKey(Subject,blank=True,null=True,on_delete=models.SET_NULL)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)    
    exam=models.ForeignKey(Exam,blank=True,null=True,on_delete=models.SET_NULL)
    MCQ1=models.IntegerField(blank=True,null=True)
    CQ1=models.IntegerField(blank=True,null=True)
    practical1=models.IntegerField(blank=True,null=True)
    total1=models.IntegerField(blank=True,null=True)
    MCQ2=models.IntegerField(blank=True,null=True)
    CQ2=models.IntegerField(blank=True,null=True)
    practical2=models.IntegerField(blank=True,null=True)
    total2=models.IntegerField(blank=True,null=True)
    total=models.IntegerField(blank=True,null=True)
    highest_mark=models.ForeignKey(HighestMarks,blank=True,null=True,on_delete=models.SET_NULL)
    grade=models.CharField(max_length=150,blank=True,null=True)
    cgpa=models.CharField(max_length=150,blank=True,null=True)
    grade_1st=models.CharField(max_length=15,blank=True,null=True)
    grade_2nd=models.CharField(max_length=15,blank=True,null=True)
     
    class Meta:
        ordering = ['group','total']
        unique_together=('class_roll','subject','exam')
    def __str__(self):
        if self.subject is not None:
            return self.class_roll+': '+self.subject.name_en
        return self.class_roll
    def subject_name(self):
        if self.subject is not None:
            return self.subject.name_en
    
    def save(self, *args, **kwargs):
        total=0
        if self.subject:
            group=Group.objects.filter(id=3).first()
            subj=Subject.objects.filter(name_en=self.subject.name_en).first()

            if group in subj.group.all():
                if self.subject.id == 3:
                    if self.CQ1:
                        total=total+self.CQ1
                        if self.CQ1<17:
                            self.grade="F"
                            self.grade_1st="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                        
                    if self.MCQ1:
                        total=total+self.MCQ1
                        if self.MCQ1<8:
                            self.cgpa=0
                            self.grade="F"
                            self.grade_1st="F"

                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                    if self.practical1:
                        total=total+self.practical1
                        if self.practical1<8:
                            self.cgpa=0
                            self.grade="F"
                            self.grade_1st="F"
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                        
                else:
                    if self.CQ1 and self.CQ2:
                        sum=self.CQ1+self.CQ2
                        total=total+sum
                        if self.CQ1<16:
                             self.grade_1st="F"
                        if sum<33:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                    if self.MCQ1 and self.MCQ2:
                        sum=self.MCQ1+self.MCQ2
                        total=total+sum
                        if self.MCQ1<8:
                             self.grade_1st="F"
                        if sum<16:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                    if self.practical1 and self.practical2:
                        sum=self.practical1+self.practical2
                        total=total+sum
                        if self.practical1<8:
                             self.grade_1st="F" 
                        if self.practical2<8:
                             self.grade_2nd="F"
                        if sum<16:
                            self.cgpa=0
                            self.grade="F"
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
            else:
                if self.subject.id==1:
                    if self.CQ1:
                        total=total+self.CQ1
                        if self.CQ1<23:
                            self.grade="F"
                            self.grade_1st="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    if self.MCQ1:
                        total=total+self.MCQ1
                        if self.MCQ1<10:
                            self.grade="F"
                            self.grade_1st="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    if self.CQ2:
                        total=total+self.CQ2
                        if self.CQ2<33:
                            self.grade="F"
                            self.grade_2nd="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                        
                elif self.subject.id==2:
                    if self.CQ1 and self.CQ2:
                        sum=self.CQ1+self.CQ2
                        total=total+sum
                        if sum<66:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                else:
                    if self.CQ1 and self.CQ2:
                        sum=self.CQ1+self.CQ2
                        total=total+sum
                        if self.CQ1<23:
                            self.grade_1st="F" 
                        if self.CQ2<23:
                            self.grade_2nd="F" 
                        if sum<46:
                            self.grade="F"
                            self.cgpa=0
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    

                    if self.MCQ1 and self.MCQ2:
                        sum=self.MCQ1+self.MCQ2
                        total=total+sum
                        if self.MCQ1<10:
                            self.grade_1st="F" 
                        if self.MCQ2<10:
                            self.grade_2nd="F" 
                        if sum<20:
                            self.cgpa=0
                            self.grade="F"
                    else:
                        self.grade="Absent"
                        self.cgpa=None
                    
                        


            self.total=total

            if self.grade == 'F':
                self.cgpa=0
            elif self.grade == 'Absent':
                self.cgpa=None
            elif self.subject.id == 3:
                if total<33:
                    self.cgpa=0
                    self.grade="F"
                elif total>=33 and total<40:
                    self.cgpa=1
                    self.grade="D"

                elif total>=40 and total<50:
                    self.cgpa=2
                    self.grade="C"
                elif total>=50 and total<60:
                    self.cgpa=3
                    self.grade="B"
                elif total>=60 and total<70:
                    self.cgpa=3.5
                    self.grade="A-"
                elif total>=70 and total<80:
                    self.cgpa=4
                    self.grade="A"
                elif total>=80 and total<=100:
                    self.cgpa=5
                    self.grade="A+"
                else:
                    self.cgpa=None
                    self.grade="Undefined"

            else: 
                if total<66:
                    self.cgpa=0
                    self.grade="F"

                elif total>=66 and total<80:
                    self.cgpa=1
                    self.grade="D"

                elif total>=80 and total<100:
                    self.cgpa=2
                    self.grade="C"
                elif total>=100 and total<120:
                    self.cgpa=3
                    self.grade="B"
                elif total>=120 and total<140:
                    self.cgpa=3.5
                    self.grade="A-"
                elif total>=140 and total<160:
                    self.cgpa=4
                    self.grade="A"
                elif total>=160 and total<=200:
                    self.cgpa=5
                    self.grade="A+"
                else:
                    self.cgpa=None
                    self.grade="Undefined"




        super(TestMarks, self).save(*args, **kwargs)



class Result(models.Model):
    class_roll=models.CharField(max_length=255,)
    name=models.CharField(max_length=255,blank=True, null=True)
    position=models.IntegerField(blank=True,null=True)
    group=models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    section=models.CharField(max_length=255,blank=True, null=True)
    exam=models.ForeignKey(Exam,blank=True,null=True,on_delete=models.SET_NULL)
    total=models.IntegerField(blank=True,null=True)
    grade=models.CharField(max_length=255,blank=True,null=True)
    cgpa=models.CharField(max_length=255,blank=True,null=True)
    number_of_subject=models.IntegerField(blank=True,null=True)
    present_at=models.IntegerField(blank=True,null=True)
    absent_at=models.IntegerField(blank=True,null=True)
    fail_at=models.IntegerField(blank=True,null=True)
    fail_at_without_4th=models.IntegerField(blank=True,null=True)
    pass_at=models.IntegerField(blank=True,null=True)
    absent_or_fail_at=models.IntegerField(blank=True,null=True)
    absent_or_fail_without_4th=models.IntegerField(blank=True,null=True)
    minimum_pass=models.IntegerField(blank=True,null=True)
    remarks=models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        ordering = ['-group','-position']
    def __str__(self):
        if self.class_roll is not None:
            return self.class_roll+': '+self.name
        return self.class_roll
    def save(self, *args, **kwargs):
        if self.absent_at != None and self.fail_at != None:
            self.absent_or_fail_at=self.absent_at +self.fail_at
        else:
            self.absent_or_fail_at=self.absent_at
        super(Result, self).save(*args, **kwargs)

