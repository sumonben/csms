
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import PaymentPurpose
from django.db.models import Q


class SearchPaymentForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))

    class Meta:
        model = PaymentPurpose
        fields = []
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('instance', None)
        super(SearchPaymentForm,self).__init__(*args,**kwargs)
        if self.current_user:
            if self.current_user.is_superuser or self.current_user.is_staff :
                self.fields['purpose']=forms.ModelChoiceField(required=True, queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1)).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
            else:
                self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1),is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
        else:
            self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1),is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))


class SearchPaymentReceiptForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))

    class Meta:
        model = PaymentPurpose
        fields = []
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('instance', None)
        super(SearchPaymentReceiptForm,self).__init__(*args,**kwargs)
        if self.current_user:
            if self.current_user.is_superuser or self.current_user.is_staff :
                self.fields['purpose']=forms.ModelChoiceField(required=True, queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1)).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
            else:
                self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1),is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
        else:
            self.fields['purpose']=forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(~Q( payment_type= 1),is_active=True).order_by('-id'),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

