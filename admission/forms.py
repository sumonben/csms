import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from payment.models import PaymentPurpose
from student.models import Session,Group

BOARD_CHOICE={
    '':'---------',
    'Dhaka':'Dhaka',
    'Rajshahi':'Rajshahi',
    'Dinajpur':'Dinajpur',
    'Madrasah':'Madrasah',    
    'BTEB':'BTEB',
    'Technical':'Technical',
    'Chattogram':'Chattogram',
    'Jashore':'Jashore',
    'Jessore':'Jessore',
    'Mymensingh':'Mymensingh',
    'Cumilla':'Cumilla',
    'Barishal':'Barishal',
    'Sylhet':'Sylhet',

}
def year_choices():
    years= [(r,r) for r in range(datetime.date.today().year-1, datetime.date.today().year+1)]
    years.reverse()
    return years

class AdmissionLoginForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}))
    passing_year= forms.ChoiceField(required=True,label="SSC Passing year",choices=year_choices,widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))
    class Meta:
        model = PaymentPurpose
        fields = []
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('instance', None)
        super(AdmissionLoginForm,self).__init__(*args,**kwargs)
        if self.current_user:
            if self.current_user.is_superuser or self.current_user.is_staff :
                self.fields['purpose']=forms.ModelChoiceField(required=True, queryset=PaymentPurpose.objects.filter( payment_type= 1).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
            else:
                self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(payment_type= 1,is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
        else:
            self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter( payment_type= 1,is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
  

class SearchAdmissionForm(forms.ModelForm):
    roll= forms.CharField(label="SSC Roll", widget=forms.TextInput( attrs={'class': 'form-control form-control-sm',}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    board= forms.ChoiceField(required=True,label="SSC Board",choices=BOARD_CHOICE,widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))
    passing_year= forms.ChoiceField(required=True,label="SSC Passing year",choices=year_choices,widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('instance', None)
        super(SearchAdmissionForm,self).__init__(*args,**kwargs)
        if self.current_user:
            if self.current_user.is_superuser or self.current_user.is_staff :
                self.fields['purpose']=forms.ModelChoiceField(required=True, queryset=PaymentPurpose.objects.filter( payment_type= 1).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
            else:
                self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(payment_type= 1,is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
        else:
            self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter( payment_type= 1,is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
  
class SelectAdmissionForm(forms.ModelForm):
    
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True,payment_type=1),initial=PaymentPurpose.objects.filter(is_active=True,payment_type=1).last(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []

class SearchIDCardForm(forms.ModelForm):
    roll_from= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    roll_to= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    session= forms.ModelChoiceField(required=True,queryset=Session.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))
    group= forms.ModelChoiceField(required=True,queryset=Group.objects.all()[0:3],widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []