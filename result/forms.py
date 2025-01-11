
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Exam

class SeachResultForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'textfieldUSERinfo','onchange' : 'myFunction(this.id)',}))
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []
