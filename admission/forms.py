import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from payment.models import PaymentPurpose

class AdmissionLoginForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True,payment_type=1),widget=forms.Select(attrs={'class': 'form-control form-control-sm','required':'true'}))

    class Meta:
        model = PaymentPurpose
        fields = []
