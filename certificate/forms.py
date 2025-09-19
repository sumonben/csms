import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Certificate,CertificateType
from student.models import Student, Department,Subject,Session,Group,Class,StudentCategory
from student.forms import year_choices
from django.db.models import Q,Count

CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),

    ]

CHOICE_CERTIFICATE=[
        ('', '----------'),
        ('1', 'প্রশংসা পত্র'),
        ('2','চরিত্রগত সনদ'),
        ('3', 'ছাড়পত্র'),
        ('4', 'অধ্যয়নরত প্রত্যয়নপত্র'),
        ('5', 'প্রত্যয়নপত্র'),

    

]


class ChoiceCertificateForm(forms.ModelForm):
    class_roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
    student_category= forms.ModelChoiceField(queryset=StudentCategory.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'ShowChangeInCategory(this.id)',}))
    certificate_type= forms.ModelChoiceField(required=True,queryset=CertificateType.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
    session= forms.ModelChoiceField(required=False,queryset=Session.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
    group= forms.ModelChoiceField(required=False,queryset=Group.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','readonly':True}))
    department= forms.ModelChoiceField(required=False,queryset=Department.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','readonly':True}))

    class Meta:
        model = Certificate
        fields = []

class CertificateForm(forms.ModelForm):
    gender= forms.CharField(
        widget=forms.RadioSelect(choices=CHOICES,),
         
    )
    def __init__(self,*args,**kwargs):
        student = kwargs.pop('student')

        type = kwargs.pop('certificate_type')

        super(CertificateForm,self).__init__(*args,**kwargs)
        self.fields['student_category']=forms.ModelChoiceField(queryset=StudentCategory.objects.filter(id=student.student_category.id),initial=StudentCategory.objects.filter(id=student.student_category.id).first(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

        if student.student_category== 1 or student.student_category== 4:
                self.fields['session']=forms.ModelChoiceField(queryset=Session.objects.all(),initial=Session.objects.last(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
                self.fields['passing_year']= forms.ChoiceField(choices=year_choices,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
                self.fields['department']=forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','style' : 'display:none',}),required=False)
                if category==1:
                    self.fields['group']=forms.ModelChoiceField(queryset=Group.objects.filter(Q(id=1)|Q(id=2)|Q(id=3)),initial=Group.objects.last(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
                else:
                    self.fields['group']=forms.ModelChoiceField(queryset=Group.objects.filter(Q(id=4)|Q(id=5)|Q(id=6)|Q(id=7)|Q(id=8)|Q(id=9)),initial=Group.objects.last(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
        else:
                self.fields['session']=forms.ModelChoiceField(queryset=Session.objects.all(),initial=Session.objects.last(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
                self.fields['passing_year']= forms.ChoiceField(choices=year_choices,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
                self.fields['department']=forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
                self.fields['group']=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','style' : 'display:none',}),required=False)
          
    class Meta:
        model = Certificate
        fields = "__all__"
        exclude=['adress','is_valid','subjects','transaction']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Name in English','onkeypress' : "myFunction(this.id)"}),
            'name_bangla': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'নাম লিখুন(বাংলায়)','onkeypress' : "myFunction(this.id)"}),
            'father_name': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Father Name in English','onkeypress' : "myFunction(this.id)"}),
            'father_name_bangla': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Father Name in Bangla','onkeypress' : "myFunction(this.id)"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Mother Name in English','onkeypress' : "myFunction(this.id)"}),
            'mother_name_bangla': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Mother Name in Bangla','onkeypress' : "myFunction(this.id)"}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Email','onkeypress' : "myFunction(this.id)"}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  '11 digits ','onkeypress' : "myFunction(this.id)"}),
            'date_of_birth': forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control form-control-sm', 'placeholder': 'Select a date','type': 'date'}),
            'class_year': forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'margin-bottom:3px;','onchange' : "studentGroup(this.id)"}),
            'birth_registration': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Birth registration Number'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'nationality'}),
            
      }

    
    

   