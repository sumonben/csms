
import datetime
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Exam

class SeachResultForm(forms.ModelForm):
    roll= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','onchange' : 'myFunction(this.id)',}))

    class Meta:
        model = Exam
        fields = []
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(SeachResultForm,self).__init__(*args,**kwargs)
        if self.current_user:
            if self.current_user.is_superuser or self.current_user.is_staff :
                self.fields['exam']=forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
            else:
                self.fields['exam']=forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
        else:
            self.fields['exam']=forms.ModelChoiceField(required=True,queryset=Exam.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))
                       

class CreateResultForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = Exam
        fields = []
class CreatePositionForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = Exam
        fields = []

class DeletResultForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = Exam
        fields = []
class HighestMarksForm(forms.ModelForm):
    exam= forms.ModelChoiceField(required=True,queryset=Exam.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm',}))

    class Meta:
        model = Exam
        fields = []
