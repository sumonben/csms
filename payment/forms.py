
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import PaymentPurpose

class SearchPaymentForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = PaymentPurpose
        fields = []

class SearchPaymentReceiptForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = PaymentPurpose
        fields = []
