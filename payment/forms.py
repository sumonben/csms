
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import PaymentPurpose

class SearchPaymentForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'textfieldUSERinfo','onchange' : 'myFunction(this.id)',}))
    purpose= forms.ModelChoiceField(required=True,queryset=PaymentPurpose.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = PaymentPurpose
        fields = []


