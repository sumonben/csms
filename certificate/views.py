from django.shortcuts import render
from .forms import ChoiceCertificateForm,CertificateForm
from student.models import Student, Group,Adress
from student.forms import AdressForm
from django.http import HttpResponse

# Create your views here.

def ChoiceCertificate(request):
    form=ChoiceCertificateForm()
    return render(request,'certificate/choice_certificate.html',{'form':form})

def CertificateFormEntry(request):
    if request.method=="POST":
        context={}
        student=Student.objects.filter(class_roll=request.POST.get('class_roll'),student_category=request.POST.get('student_category')).last()
        context['student']=student
        if student:
            if student.permanent_adress and student.guardian_info:
                if request.POST.get('certificate_type') == "2":
                    return render(request,'certificate/certificates/hsc_current_student_certificate.html',context=context)


        form=CertificateForm(student=student,certificate_type=request.POST.get('certificate_type'))
        adress_form = AdressForm()
        certificate_type=request.POST.get('certificate_type')
        context={'form':form,'adress_form':adress_form}
        context['student']=student
        context['choice_certificate']=certificate_type
        if request.POST.get('student_category') == 1:
            group=Group.objects.filter(id=request.POST.get('group')).first()
            subject_form=SubjectChoiceForm(group=group)
            context['subject_form']=subject_form
            return render(request,'certificate/certificate_form_entry_hsc.html',context=context)
        return render(request,'certificate/certificate_form_entry_all.html',context=context)
    return HttpResponse("This is not POST")

