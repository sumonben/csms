from django.http import JsonResponse
from django.shortcuts import render,redirect
from student.forms import StudentForm,AdressForm,PresentAdressForm,SscEquvalentForm,SubjectChoiceForm,GuardianForm
from student.models import Group,Student,Session,SubjectChoice,SscEquvalent,StudentCategory,Division,District,Upazilla,Union
from django.contrib.auth import get_user_model
from sslcommerz_lib import SSLCOMMERZ
from payment import sslcommerz 
from .forms import AdmissionLoginForm,SearchAdmissionForm
from .models import StudentAdmission
from payment.models import PaymentPurpose
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
import random
import string


def generate_student_id( size=8, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))

UserModel=get_user_model()
board={
    'DHA':'Dhaka',
    'RAJ':'Rajshahi',
    'CHA':'Chattogram',
    'DIN':'Dinajpur',
}
# Create your views here.
def admissionLogin(request ):
    form = AdmissionLoginForm()
    return render(request, 'admission/admission_login.html',{'form':form})
# Create your views here.
# Create your views here.

def admissionForm(request):
    if request.POST.get('username') and request.POST.get('password') :
        str=request.POST.get('username')
        str1=request.POST.get('password')
        str=str[6:9]
        if str in board:
            try:
                str=board[str]
            except():
                return redirect('admission_login')


        str2=request.POST.get('purpose')
        student=StudentAdmission.objects.filter(ssc_roll=str1,board=str,status="Not Admitted").last()
        if student:
            try:
                #student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('password'),board=board[str[-3:]],status='Not Admitted').first()
                payment_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
                group=Group.objects.filter(title_en=student.group).first()
                print('Student: ',student.group)
                if group:
                    form = StudentForm(instance=student)
                    subject_form = SubjectChoiceForm(group=group)
                    adress_form = AdressForm()
                    present_adress_form = AdressForm()
                    ssc_equivalent_form=SscEquvalentForm()
                    guardian_form=GuardianForm()
                    print(group.title_en)
                    return render(request, 'admission/admission.html',{'payment_purpose':payment_purpose,'group':group,'form':form,'subject_form':subject_form,'adress_form':adress_form,'ssc_equivalent_form':ssc_equivalent_form,'guardian_form':guardian_form,'present_adress_form':present_adress_form})
                    

                else:
                    subject_form = None
                    return redirect('admission_login')
            except():
                print("Exception")
                return redirect('admission_login')

            
    return redirect('admission_login')


        



def admissionFormSubmit(request):
    
    context ={}

    data = {}
    #student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('password'),board=board[str[-3:]],status='Not Admitted').first()
    flag1=0
    flag2=0
    flag3=0
    if request.method=='POST':
        group=None
        print("got it")
        student_form=None
        print(request.POST.get('name'))
        email=request.POST.get('email')
        username=request.POST.get('phone')
        last_name='student'
        password='Student@'+request.POST.get('phone')
        if UserModel.objects.filter(email=email).exists() is True:
            email='Email already exist in user system!! '
            context['email']=email
            print('1',email,username)
            
        if UserModel.objects.filter(username=username).exists() is True:
            phone='Phone number already exist in user system!! '
            context['phone']=phone
            print('2',email,username)
            
        if bool(context):
            print('5',email,username)
            return JsonResponse({'context': context},safe=False)
        

        form = StudentForm(request.POST, request.FILES)
        ssc_equivalent_form = SscEquvalentForm(request.POST)
        guardin_form = GuardianForm(request.POST)
        adress_form = AdressForm(request.POST)
        

        if form.is_valid():
            student_form=form.save(commit=False)
            student_form.gender=request.POST.get('gender')
            
            group=Group.objects.filter(title_en=request.POST.get('admission_group')).first()
            student_form.group=group
            session=Session.objects.first()
            student=Student.objects.filter(is_active=True).last()
            student_form.class_roll=generate_student_id()

            # std_count=Student.objects.filter(group=group,session=session).count()
            # print(session)
            # session_string=session.title_en
            # str1=session_string[-5:-3]
            # roll=int(str1)*10000
            # print(roll)
            # if group.title_en in 'Science':
            #     s_roll=roll+1001+std_count
            #     section=s_roll-roll
            #     if section<= 1250:
            #         student_form.section='A'
            #     elif section> 1250 and section<= 1550:
            #         student_form.section='B'
            #     else:
            #         student_form.section='C'
            #     print(s_roll)
            #     student_form.class_roll=str(s_roll)

            # if group.title_en in 'Humanities':
            #     s_roll=roll+2001+std_count
            #     section=s_roll-roll
            #     if section<= 2250:
            #         student_form.section='A'
            #     elif section> 2250 and section<= 2550:
            #         student_form.section='B'
            #     else:
            #         student_form.section='C'
            #     student_form.class_roll=str(s_roll)
            # if group.title_en in 'Business Studies':
            #     s_roll=roll+3001+std_count
            #     section=s_roll-roll
            #     student_form.section='A'
               
            #     student_form.class_roll=str(s_roll)
            
            if guardin_form.is_valid():
                guardin=guardin_form.save()
                student_form.guardian_info=guardin
            if adress_form.is_valid:
                adress=adress_form.save()
                student_form.permanent_adress=adress
                
            
            
            student_category=StudentCategory.objects.filter(title_en="HSC").first()
            student_form.student_category=student_category
            student_form.save()

            print('6. Student form',email,username,student)
        print(form.errors)
        print(group)
        subject_form = SubjectChoiceForm(request.POST,group=group)


            
        if ssc_equivalent_form.is_valid():
                ssc_form=ssc_equivalent_form.save(commit=False)
                ssc_form.student=student_form
                if ssc_form.student:
                    ssc_form.save()
        '''if guardin_form.is_valid():
                guardian=guardin_form.save(commit=False)
                guardian.student=student_form
                guardian.save()'''
        if subject_form.is_valid():
                for terminal in subject_form.cleaned_data['compulsory_subject']:
                    print(terminal)
                subject=subject_form.save(commit=False)
                subject.student=student_form
                subject=subject_form.save()
                compulsory_sub=subject_form.cleaned_data['compulsory_subject']
                for i in compulsory_sub:
                    subject.compulsory_subject.add(i)
                if group.title_en not in 'Business Studies':
                    optional_sub=subject_form.cleaned_data['optional_subject']
                    for i in optional_sub:
                        subject.optional_subject.add(i)
                    if subject.student:
                        subject.save()

        print(subject_form.errors)

        cradentials = {'store_id': 'israb672a4e32dfea5',
            'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
            
        sslcommez = SSLCOMMERZ(cradentials)
        body = {}
        body['student'] = request.POST.get('name')
        body['total_amount'] = 3500
        body['currency'] = "BDT"
        body['tran_id'] = sslcommerz.generator_trangection_id()
        body['success_url'] = 'http://localhost:8000/payment/success/'
        body['fail_url'] = 'https://localhost:8000/payment/failed/'
        body['cancel_url'] = 'https://localhost:8000/payment/canceled'
        body['emi_option'] = 0
        body['cus_name'] = request.POST.get('name')
        body['cus_email'] = 'request.data["email"]'
        body['cus_phone'] = request.POST.get('phone')
        body['cus_add1'] = 'request.data["address"]'
        body['cus_city'] = 'request.data["address"]'
        body['cus_country'] = 'Bangladesh'
        body['shipping_method'] = "NO"
        body['multi_card_name'] = ""
        body['num_of_item'] = 1
        body['product_name'] = "Test"
        body['product_category'] = "Test Category"
        body['product_profile'] = "general"
        body['value_a'] = student_form.class_roll
        body['value_b'] = student_form.name
        body['value_c'] = student_form.phone
        body['value_d'] = 1          
        response = sslcommez.createSession(body)
        print(response["sessionkey"])   


      
        return redirect('https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"])

def formDownload(request):
        phone=request.POST.get('student_id')
        print("sumon",phone)

        student=Student.objects.filter(phone=phone).first()
        subject_choice=SubjectChoice.objects.filter(student=student).first()
        
        ssc_equivalent=SscEquvalent.objects.filter(student=student).first()


        return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice})

def SubprocessesView(request):
        print(request.GET.get('id'),request.GET.get('value'))
        if request.GET.get('id')=='id_division':
            division=Division.objects.filter(id=request.GET.get('value')).first()
            district=District.objects.filter(division=division)
            district=list(district.values())
            print(district)
        if request.GET.get('id')=='id_district':
            division=District.objects.filter(id=request.GET.get('value')).first()
            print(division)
            district=Upazilla.objects.filter(district=division)
            district=list(district.values())
            print(district)
        return JsonResponse({'status': 'success','meaasge':'Account created Successfully','district':district},safe=False)

class SearchAdmissionView(View):
    template_name = 'admission/search_admission_form.html'
    
    def get(self, request, *args, **kwargs):
        context={}
        form=SearchAdmissionForm()
        context['form'] = form
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        context={}
        roll=request.POST.get('roll').strip()
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).last()
        if student is None:
            form=SearchAdmissionForm()
            context['notfound']="Student Not Found, Please complete admission proccess!"
            context['form'] = form
            return render(request, self.template_name,context)
        subject_choice=SubjectChoice.objects.filter(student=student).first()
        ssc_equivalent=SscEquvalent.objects.filter(student=student).first()
        return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice})
