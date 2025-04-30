import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
# import GeeksModel from models.py
from .models import Student,SubjectChoice,Upazilla,District,Division,Adress,SscEquvalent,GuardianInfo,Subject,Session,Group,Class
from django.db.models import Q,Count
from payment.models import PaymentPurpose
from django_select2.forms import ModelSelect2Widget
# create a ModelForm
MARITAL_CHOICES = [('Unmarried', 'Unmarried'),('Married', 'Married'),('Divorced','Divorced')]
BlOOD_CHOICE=[('AB+', 'AB+'),('A+', 'A+'),('B+', 'B+'),('O+', 'O+'),('AB-', 'AB-'),('A-', 'A-'),('B-', 'B-'),('O-', 'O-'),]
        
def year_choices():
    return [(r,r) for r in range(2009, datetime.date.today().year+1)]

CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),

    ]    
BOARD_CHOICE=[
        ('Dhaka', 'Dhaka'),
        ('Rajshahi', 'Rajshahi'),
        ('Chattogram', 'Chattogram'),
        ('Khulna', 'Khulna'),
        ('Barisal', 'Barisal'),
        ('Dinajpur', 'Dinajpur'),
        ('Jassore', 'Jassore'),
        ('Mymensing', 'Mymensing'),
        ('Sylhet', 'Sylhet'),
        ('Cumilla', 'Cumilla'),
        ('Madrasah', 'Madrasah'),
        ('Technical', 'Technical'),
        ('Vocationnal', 'Vocationnal'),

]
DEGREE_CHOICE=[
        ('SSC', 'SSC'),
        ('Dakhil', 'Dakhil'),
        ('Technical', 'Technical'),

]
RELIGION_CHOICES=[
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Christanity', 'Christanity'),
        ('Buddhism', 'Buddhism'),


]
FATHER_PROFESSION_CHOICE = [
        ('Agriculture Farming', 'Agriculture Farming'),
        ('Business', 'Business'),
        ('Govt. Service', 'Govt. Service'),
        ('NonGovt. Service', 'NonGovt. Service'),

        ]
MOTHER_PROFESSION_CHOICE = [
        ('House Wife', 'House Wife'),
        ('Business', 'Business'),
        ('Govt. Service', 'Govt. Service'),
        ('NonGovt. Service', 'NonGovt. Service'),

        ]
        
class StudentForm(forms.ModelForm):
    session=forms.ModelChoiceField(queryset=Session.objects.all(),initial=Session.objects.first(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))


    class Meta:
        MARITAL_CHOICES = [('Unmarried', 'Unmarried'),('Married', 'Married'),('Divorced','Divorced')]
        BlOOD_CHOICE=[('AB+', 'AB+'),('A+', 'A+'),('B+', 'B+'),('O+', 'O+'),('AB-', 'AB-'),('A-', 'A-'),('B-', 'B-'),('O-', 'O-'),]
        model = Student
        fields = "__all__"
        exclude=['std_id','class_roll','exam_roll','registration','passing_year','student_category','department','section','class_year','cgpa','guardian_info','present_adress','permanent_adress','user','is_active','fourth_subject']
        #department=forms.ModelChoiceField(label="",queryset=Department.objects.all(),empty_label="Placeholder",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  'Name in English','onkeypress' : "myFunction(this.id)",'value':'sumon'}),
            'name_bangla': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'নাম লিখুন(বাংলায়)','onkeypress' : "myFunction(this.id)",'value':'sumon'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Email','onkeypress' : "myFunction(this.id)",'value':'sumo@gmail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  '11 digits ','onkeypress' : "myFunction(this.id)",'value':'01712534564'}),
            'date_of_birth': forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control form-control-sm', 'placeholder': 'Select a date','type': 'date'}),
            'group': forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'margin-bottom:3px;','onchange' : "studentGroup(this.id)"}),
            'birth_registration': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Birth registration Number'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'nationality'}),
            'blood_group': forms.Select(choices=BlOOD_CHOICE,attrs={'class': 'form-control form-control-sm', 'placeholder':  'Your blood group'}),
            'marital_status': forms.Select(choices=MARITAL_CHOICES,attrs={'class': 'form-control form-control-sm',}),
            'religion': forms.Select(choices=RELIGION_CHOICES,attrs={'class': 'form-control form-control-sm',}),
            'gender': forms.Select(choices=CHOICES,attrs={'class': 'form-control form-control-sm',}),
            

      }    
    def __init__(self, *args, **kwargs):
            payment_type = kwargs.pop('instance', None)
            super(StudentForm, self).__init__(*args, **kwargs)

        
   
        

class GuardianForm(forms.ModelForm):
    

    class Meta:
        model = GuardianInfo
        fields = "__all__"
        exclude=['serial',]

        
        widgets = {
            'father_name_en': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Name in English','onkeypress' : "myFunction(this.id)"}),
            'father_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'নাম লিখুন(বাংলায়)','onkeypress' : "myFunction(this.id)"}),
            'profession_of_father': forms.Select(choices=FATHER_PROFESSION_CHOICE,attrs={'class': 'form-control form-control-sm', 'placeholder':  'Email','onkeypress' : "myFunction(this.id)"}),
            'father_nid': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  '11 digits ','onkeypress' : "myFunction(this.id)"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'নাম লিখুন(বাংলায়)','onchange' : "myFunction(this.id)"}),
            'mother_name_en': forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':  'Name in English'}),
            'profession_of_mother': forms.Select(choices=MOTHER_PROFESSION_CHOICE,attrs={'class': 'form-control form-control-sm', 'style': 'margin-bottom:3px;','required':'true'}),
            'mother_nid': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Mother NID Number'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'placeholder':  '11 digits '}),
            'anual_income': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Anual Family Income'}),
           


      }
  
class SubjectChoiceForm(forms.ModelForm):
    #compulsory_subject=forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),initial=Subject.objects.filter(serial__in=[ 1, 2,3]), widget=FilteredSelectMultiple('Subject',False, attrs={'class':'form-control form-control-sm'}))
    
    #optional_subject=forms.ModelMultipleChoiceField(Subject.objects.all(), widget=FilteredSelectMultiple('Optional Subject',False, attrs={'row':'1','class': 'form-control form-control-sm',}))
    #group= forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'}))

    class Meta:
        model = SubjectChoice
        fields = "__all__"
        exclude=['serial','student']
        widgets={
                        'fourth_subject': forms.Select(attrs={'class': 'form-control form-control-sm','onclick' : "fourthSubject(this.id);",'style':'margin-bottom:20px'}),

        }
        
    class Media:
            css = {
                'all': ('/static/admin/css/widgets.css',),
            }
            js = ('/admin/jsi18n',)
        
    def clean_compulsory_subject(self):
            compulsory_subject = self.cleaned_data['compulsory_subject']
            return compulsory_subject
        
    def __init__(self,*args,**kwargs):
        
        group = kwargs.pop('group')
        super(SubjectChoiceForm,self).__init__(*args,**kwargs)
        if group:
            if group.title_en=="Science":
                self.fields['compulsory_subject']=forms.ModelMultipleChoiceField(queryset=Subject.objects.filter(Q(group=group)|Q(group=None)),initial=Subject.objects.filter(serial__in=[ 1, 2,3,4,5,]), widget=FilteredSelectMultiple('Comulsory Subject',True, attrs={'class':'form-control form-control-sm',}))
                self.fields['optional_subject']=forms.ModelMultipleChoiceField(queryset=Subject.objects.filter(group=group, type='Fourth'), widget=FilteredSelectMultiple('Optional Subject',False, attrs={'class':'form-control form-control-sm',}))
 
            if group.title_en=="Humanities":
                self.fields['compulsory_subject']=forms.ModelMultipleChoiceField(queryset=Subject.objects.filter(Q(group=group)|Q(group=None)),initial=Subject.objects.filter(serial__in=[ 1, 2,3,8]), widget=FilteredSelectMultiple('Comulsory Subject',True, attrs={'class':'form-control form-control-sm',}))
                self.fields['optional_subject']=forms.ModelMultipleChoiceField(queryset=Subject.objects.filter(group=group, type='Optional'), widget=FilteredSelectMultiple('Optional Subject',False, attrs={'class':'form-control form-control-sm',}))
                self.fields['fourth_subject']=forms.ModelChoiceField(queryset=Subject.objects.filter(group=group, type='Optional'), widget=forms.Select( attrs={'class':'form-control form-control-sm',}))
            if group.title_en=="Business Studies":
                self.fields['compulsory_subject']=forms.ModelMultipleChoiceField(queryset=Subject.objects.filter(Q(group=group)|Q(group=None)),initial=Subject.objects.filter(serial__in=[ 1, 2,3,13,14,16]), widget=FilteredSelectMultiple('Comulsory Subject',True, attrs={'class':'form-control form-control-sm',}))
                self.fields['fourth_subject']=forms.ModelChoiceField(queryset=Subject.objects.filter(serial__in=[9,]),initial=Subject.objects.filter(serial__in=[ 9,]), widget=forms.Select( attrs={'class':'form-control form-control-sm',}))
                if 'optional_subject' in self.fields: del self.fields['optional_subject']
                #self.fields['compulsory_subject'].initial=Subject.objects.filter(serial__in=[ 1, 2,3])
                #self.fields['compulsory_subject'].widget = FilteredSelectMultiple('Subject',False, attrs={'class':'form-control form-control-sm'})

            
        
class AdressForm(forms.ModelForm):
    division= forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
    district=forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
    upazilla= forms.ModelChoiceField(queryset=Upazilla.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
             
    class Meta:
        model = Adress
        fields = "__all__"
        exclude=['serial']

        
        widgets = {
            'village_or_house': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Village Name/house No.','onkeypress' : "myFunction(this.id);",'label':'Village/house'}),
            'house_or_street_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Street Name/No.','onkeypress' : "myFunction(this.id);",'label':'Street No.'}),
            'post_office': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Bogura-5800','onkeypress' : "myFunction(this.id);"}),
            'division': forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : "myFunctionTeacher(this.id);"}),
            'district': forms.Select(attrs={'class': 'form-control form-control-sm','onchange' : "myFunctionTeacher(this.id);"}),            
            'upazilla': forms.Select(attrs={'class': 'form-control form-control-sm',}),


        }
class PresentAdressForm(forms.ModelForm):
    division= forms.ModelChoiceField(queryset=Division.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
    district=forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
    upazilla= forms.ModelChoiceField(queryset=Upazilla.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'})),
            
    class Meta:
        model = Adress
        fields = "__all__"
        exclude=['serial']

        
        widgets = {
            'village_or_house': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Village Name/house No.','onkeypress' : "myFunction(this.id);",'label':'Village/house'}),
            'house_or_street_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Street Name/No.','onkeypress' : "myFunction(this.id);",'label':'Street No.'}),
            'post_office': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'Bogura-5800','onkeypress' : "myFunction(this.id);"}),
            'division': forms.Select(attrs={'class': 'form-control form-control-sm',}),
            'district': forms.Select(attrs={'class': 'form-control form-control-sm',}),            
            'upazilla': forms.Select(attrs={'class': 'form-control form-control-sm',}),



        }

'''class SscEquvalentForm(forms.Form):
    
    ssc_or_equvalent= forms.ChoiceField(choices=DEGREE_CHOICE,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    ssc_group=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    ssc_board= forms.ChoiceField(choices=BOARD_CHOICE,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    ssc_session=forms.ModelChoiceField(queryset=Session.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    ssc_exam_roll= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    ssc_regitration_no=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    ssc_cgpa_with_4th= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    ssc_cgpa_without_4th=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    ssc_passing_year=forms.ChoiceField(choices=year_choices,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))'''
    
class SscEquvalentForm(forms.ModelForm):
    
    # group=forms.ModelChoiceField(label="",queryset=Group.objects.all().values_list('id', 'title_en'),widget=forms.Select(attrs={'class':'form-control form-control-sm'}),empty_label="Placeholder",)
    # session=forms.ModelChoiceField(label="",queryset=Session.objects.all().values_list('id', 'title_en'),widget=forms.Select(attrs={'class':'form-control form-control-sm'}),empty_label="Placeholder",)
    ssc_passing_year= forms.ChoiceField(choices=year_choices,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))

    class Meta:
        model = SscEquvalent
        fields = "__all__"
        exclude=['serial','student']

        
        widgets = {
            'ssc_or_equvalent': forms.Select(choices=DEGREE_CHOICE,attrs={'class': 'form-control form-control-sm','onkeypress' : "myFunction(this.id);"}),
            'ssc_board': forms.Select(choices=BOARD_CHOICE,attrs={'class': 'form-control form-control-sm','onkeypress' : "myFunction(this.id)"}),
            'ssc_group': forms.Select(attrs={'class': 'form-control form-control-sm','onkeypress' : "myFunction(this.id);",'required':'true'}),
            'ssc_session': forms.Select(attrs={'class': 'form-control form-control-sm','onkeypress' : "myFunction(this.id);",'required':'true'}),
            'ssc_exam_roll': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'SSC/Equivalent Roll'}),
            'ssc_regitration_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':  'SSC/Equivalent Registration'}),
            'ssc_cgpa_with_4th': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'CGPA with 4th Subject'}),
            'ssc_cgpa_without_4th': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'CGPA without 4th Subject'}),
            }