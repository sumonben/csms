import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from payment.models import PaymentPurpose
from student.models import Session,Group

class AdmissionLoginForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True,payment_type=1),widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []

class SearchAdmissionForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True,payment_type=1),widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []
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