
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Exam

class SeachResultForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'textfieldUSERinfo','onchange' : 'myFunction(this.id)',}))
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []
class CreateResultForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []
class CreatePositionForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []

class DeletResultForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []
class HighestMarksForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'textfieldUSERinfo',}))

    class Meta:
        model = Exam
        fields = []
