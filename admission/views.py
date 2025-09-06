from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from student.forms import StudentForm,AdressForm,PresentAdressForm,SscEquvalentForm,SubjectChoiceForm,GuardianForm
from student.models import Group,Student,Session,SubjectChoice,SscEquvalent,StudentCategory,Division,District,Upazilla,Union,Adress
from django.contrib.auth import get_user_model
from sslcommerz_lib import SSLCOMMERZ
from payment import sslcommerz 
from .forms import AdmissionLoginForm,SearchAdmissionForm,SelectAdmissionForm,SearchIDCardForm
from .models import StudentAdmission
from student.forms import AdressFormSet
from payment.models import PaymentPurpose
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from payment.sslcommerz import sslcommerz_payment_gateway_admission
import random
import string
import os
from django.contrib import messages 


def generate_student_id( size=8, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))

UserModel=get_user_model()
board={
    'DHA':'Dhaka',
    'RAJ':'Rajshahi',
    'DIN':'Dinajpur',
    'MAD':'Madrasah',    
    'BTE':'BTEB',
    'TEC':'Technical',
    'CHA':'Chattogram',
    'JAS':'Jashore',
    'JES':'Jessore',
    'MYM':'Mymensingh',
    'CUM':'Cumilla',
    'BAR':'Barishal',
    'SYL':'Sylhet',
    'BOU':'BOU',


}
def admissionLogin(request ):
    form = AdmissionLoginForm(instance=request.user)
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
                messages.success(request, "Your creadential doesn't match!!")
                return redirect('admission_login')


        str2=request.POST.get('purpose')
        payment_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        student=StudentAdmission.objects.filter(ssc_roll=str1,board=str,admission_session__in=payment_purpose.sessions.all()).last()
        if student:
            if student.status == "Admitted":
                messages.error(request, 'Your Admssion already done, you can download admission form!')
                return redirect('search_admission_form')
 
            try:
                context={}
                #student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('password'),board=board[str[-3:]],status='Not Admitted').first()
                group=Group.objects.filter(title_en=student.admission_group).first()
                if group:
                    select_admission=SelectAdmissionForm()
                    form = StudentForm(instance=student)
                    subject_form = SubjectChoiceForm(group=group)
                    adress_formset = AdressFormSet(queryset=Adress.objects.none())
                    adress_form = AdressForm()
                    present_adress_form = AdressForm()
                    ssc_equivalent_form=SscEquvalentForm(instance=student)
                    guardian_form=GuardianForm()
                    context={'payment_purpose':payment_purpose,'group':group,'form':form,'subject_form':subject_form,'adress_form':adress_form,'ssc_equivalent_form':ssc_equivalent_form,'guardian_form':guardian_form,'present_adress_form':present_adress_form}
                    context['adress_formset']=adress_formset
                    return render(request, 'admission/admission.html',context)      
    
                else:
                    subject_form = None
                    messages.success(request, "Your creadential doesn't match!!")
                    return redirect('admission_login')
            except():
                print("Exception")
                messages.success(request, "Your creadential doesn't match!!")
                return redirect('admission_login')

    messages.success(request, "Your creadential doesn't match!!")       
    return redirect('admission_login')


        



def admissionFormSubmit(request):
    
    context ={}

    data = {}
    flag1=0
    flag2=0
    flag3=0
    if request.method=='POST':
        # return HttpResponse(request.POST.get('ssc_board'))
        # student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('ssc_exam_roll'),board=request.POST.get('ssc_board'),status='Not Admitted').first()
        # return HttpResponse(student)
        group=None
        print("got it")
        student_form=None
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
        
        tran_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        group=Group.objects.filter(title_en=request.POST.get('admission_group')).first()
        tran_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        ssc_equivalent=SscEquvalent.objects.filter(ssc_exam_roll=request.POST.get('ssc_exam_roll'),ssc_group=request.POST.get('ssc_group'),ssc_board=request.POST.get('ssc_board'),ssc_passing_year=request.POST.get('ssc_passing_year')).first()
        if ssc_equivalent:
            student_admission=StudentAdmission.objects.filter(ssc_roll=ssc_equivalent.ssc_exam_roll, board=ssc_equivalent.ssc_board,passing_year=ssc_equivalent.ssc_passing_year,group=ssc_equivalent.ssc_group).first()
            if  student_admission.status== "Not Admitted":
                    if ssc_equivalent.student:
                        student=Student.objects.filter(id=ssc_equivalent.student.id,is_active=False).first()
                        if student:
                            if student.image:  # Check if an image exists
                                image = student.image.path
                                if os.path.exists(image):
                                    os.remove(image)
                            student.delete()
                    # select_admission=SelectAdmissionForm()
                    # form = StudentForm(instance=student_admission)
                    # group=Group.objects.filter(title_en=student_admission.admission_group).first()
                    # subject_form = SubjectChoiceForm(group=group)
                    # adress_formset = AdressFormSet(queryset=Adress.objects.none())
                    # adress_form = AdressForm()
                    # present_adress_form = AdressForm()
                    # ssc_equivalent_form=SscEquvalentForm(instance=student_admission)
                    # guardian_form=GuardianForm()
                    # context={'payment_purpose':tran_purpose,'group':group,'form':form,'subject_form':subject_form,'adress_form':adress_form,'ssc_equivalent_form':ssc_equivalent_form,'guardian_form':guardian_form,'present_adress_form':present_adress_form}
                    # context['adress_formset']=adress_formset
                    # return render(request, 'admission/admission.html',context)
                #return redirect(sslcommerz_payment_gateway_admission(request, student,tran_purpose))
            else:
                messages.error(request, 'Your Admission already done, you can download receipt!')
                return redirect('search_admission_form')

        form = StudentForm(request.POST, request.FILES)
        ssc_equivalent_form = SscEquvalentForm(request.POST)
        guardin_form = GuardianForm(request.POST)
        formset = AdressFormSet(data=request.POST)
        adress_form = AdressForm(request.POST)
        subject_form = SubjectChoiceForm(request.POST,group=group)
        if form.is_valid():
            student_form=form.save(commit=False)
            student_form.gender=request.POST.get('gender')
            student_form.group=group
            student_form.class_roll=generate_student_id()
            student_form.std_id=student_form.class_roll
            session=Session.objects.first()
            # std_count=Student.objects.filter(group=group,session=session).count()
            # print(session)
            # session_string=session.title_en
            # str1=session_string[-2:]
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
            if formset.is_valid():
                adresses=formset.save()
                for index, adress in enumerate(adresses):
                    adress.save()
                    if index == 0:
                        student_form.permanent_adress=adress
                    else:
                        student_form.present_adress=adress

            # if adress_form.is_valid:
            #     adress=adress_form.save()
            #     student_form.permanent_adress=adress
                
            
            
            student_category=StudentCategory.objects.filter(title_en="HSC").first()
            student_form.student_category=student_category
            student_form.guardian_info.serial=int(student_form.class_roll)
            student_form.save()

            # print('6. Student form',email,username)
        # print(form.errors)
        # print(group)
            
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
                subject.class_roll=student_form.class_roll
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

        return redirect(sslcommerz_payment_gateway_admission(request, student_form,tran_purpose))
        # cradentials = {'store_id': 'israb672a4e32dfea5',
        #     'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
        # cradentials = {'store_id': 'gmrwcedubdlive',
        #     'store_pass': '677CD7B61AB5A81511', 'issandbox': False}    
        # sslcommez = SSLCOMMERZ(cradentials)
        # body = {}
        # body['student'] = request.POST.get('name')
        # body['total_amount'] = 10
        # body['currency'] = "BDT"
        # body['tran_id'] = sslcommerz.generator_trangection_id()
        # body['ipn_url'] = 'https://student.gmrwc.edu.bd/payment/ipn/'
        # body['fail_url'] = 'https://student.gmrwc.edu.bd/payment/failed/'
        # body['cancel_url'] = 'https://student.gmrwc.edu.bd/payment/canceled/'
        # body['success_url'] = 'https://student.gmrwc.edu.bd/payment/success/'
        # body['emi_option'] = 0
        # body['cus_name'] = request.POST.get('name')
        # body['cus_email'] = 'request.data["email"]'
        # body['cus_phone'] = request.POST.get('phone')
        # body['cus_add1'] = 'request.data["address"]'
        # body['cus_city'] = 'request.data["address"]'
        # body['cus_country'] = 'Bangladesh'
        # body['shipping_method'] = "NO"
        # body['multi_card_name'] = ""
        # body['num_of_item'] = 1
        # body['product_name'] = "Test"
        # body['product_category'] = "Test Category"
        # body['product_profile'] = "general"
        # body['value_a'] = student_form.class_roll
        # body['value_b'] = student_form.name
        # body['value_c'] = student_form.phone
        # body['value_d'] = 1          
        # response = sslcommez.createSession(body)
      


        # #return redirect["GatewayPageURL"]

        # return redirect('https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"])

def formDownload(request):
        phone=request.POST.get('student_id')
        print("sumon",phone)

        student=Student.objects.filter(phone=phone).first()
        subject_choice=SubjectChoice.objects.filter(student=student).first()
        
        ssc_equivalent=SscEquvalent.objects.filter(student=student).first()


        return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice})

def SubprocessesView(request):
        if request.POST.get('id') == 'id_form-0-division':
            division=Division.objects.filter(id=request.POST.get('value')).first()
            district=District.objects.filter(division=division)
            district=list(district.values())
        if request.POST.get('id') == 'id_form-1-division':
            division=Division.objects.filter(id=request.POST.get('value')).first()
            district=District.objects.filter(division=division)
            district=list(district.values())

        if request.POST.get('id') == 'id_form-0-district':
            division=District.objects.filter(id=request.POST.get('value')).first()
            upazilla=Upazilla.objects.filter(district=division)
            district=list(upazilla.values())
        if request.POST.get('id') == 'id_form-1-district':
            division=District.objects.filter(id=request.POST.get('value')).first()
            upazilla=Upazilla.objects.filter(district=division)
            district=list(upazilla.values())

        return JsonResponse({'status':'success','meaasge':'Account created Successfully','district':district},safe=False)

class SearchAdmissionView(View):
    template_name = 'admission/search_admission_form.html'
    
    def get(self, request, *args, **kwargs):
        context={}
        form=SearchAdmissionForm(instance=request.user)
        context['form'] = form
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        context={}
        roll=request.POST.get('roll').strip()
        ssc_equivalent=SscEquvalent.objects.filter(ssc_exam_roll=request.POST.get('roll').strip(),ssc_board=request.POST.get('board').strip(),ssc_passing_year=request.POST.get('passing_year')).last()
        student=None
        if ssc_equivalent:
            if ssc_equivalent.student:
                student=Student.objects.filter(id=ssc_equivalent.student.id,is_active=True).last()
                subject_choice=SubjectChoice.objects.filter(student=ssc_equivalent.student).last()
                subject_choices=[]
                for subject in subject_choice.compulsory_subject.all():
                    subject_choices.append(subject)
                for subject in subject_choice.optional_subject.all():
                    subject_choices.append(subject)        
                return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice, 'subject_choices':subject_choices})
            else:
                form=SearchAdmissionForm(instance=request.user)
                context['notfound']="Active Student Not Found, Please complete your admission proccess!"
                context['form'] = form
                return render(request, self.template_name,context)
        form=SearchAdmissionForm(instance=request.user)
        context['notfound']="Active Student Not Found, Please complete your admission proccess or contact office!"
        context['form'] = form
        return render(request, self.template_name,context)

               
class IDCardView(View):
    template_name = 'admission/get_id_card.html'
    
    def get(self, request, *args, **kwargs):
        context={}
        form=SearchIDCardForm()
        context['form'] = form
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        context={}
        roll_from=request.POST.get('roll_from').strip()
        roll_to=request.POST.get('roll_to').strip()
        group=request.POST.get('group').strip()
        session=request.POST.get('session').strip()
        student1=Student.objects.filter(class_roll=request.POST.get('roll_from').strip()).last()
        student2=Student.objects.filter(class_roll=request.POST.get('roll_to').strip()).last()
        students=None
        if student1 and student2:
            students=Student.objects.filter(id__range=(student1.id,student2.id),session=session,group=group)
        if students is None:
            form=SearchIDCardForm()
            context['notfound']="Student Not Found, Please complete admission proccess!"
            context['form'] = form
            return render(request, self.template_name,context)
        context['students'] = students
        context['session'] = "form"
        context['form'] = "form"


        return render(request, 'admission/student_id_card.html',context)





# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render,redirect
# from student.forms import StudentForm,AdressForm,PresentAdressForm,SscEquvalentForm,SubjectChoiceForm,GuardianForm
# from student.models import Group,Student,Session,SubjectChoice,SscEquvalent,StudentCategory,Division,District,Upazilla,Union,Adress
# from django.contrib.auth import get_user_model
# from sslcommerz_lib import SSLCOMMERZ
# from payment import sslcommerz 
# from .forms import AdmissionLoginForm,SearchAdmissionForm,SelectAdmissionForm,SearchIDCardForm
# from .models import StudentAdmission
# from student.forms import AdressFormSet
# from payment.models import PaymentPurpose
# from django.views.generic import View, TemplateView, DetailView
# from django.views.generic.edit import FormView
# from django.template.loader import render_to_string
# from payment.sslcommerz import sslcommerz_payment_gateway_admission
# import random
# import string
# from django.contrib import messages


# def generate_student_id( size=8, chars=string.digits):
#     return "".join(random.choice(chars) for _ in range(size))

# UserModel=get_user_model()
# board={
#     'DHA':'Dhaka',
#     'RAJ':'Rajshahi',
#     'DIN':'Dinajpur',
#     'MAD':'Madrasah',    
#     'BTE':'BTEB',
#     'TEC':'Technical',
#     'CHA':'Chattogram',
#     'JAS':'Jashore',
#     'JES':'Jessore',
#     'MYM':'Mymensingh',
#     'CUM':'Cumilla',
#     'BAR':'Barishal',
#     'SYL':'Sylhet',

# }
# # Create your views here.
# def admissionLogin(request ):
#     form = AdmissionLoginForm()
#     return render(request, 'admission/admission_login.html',{'form':form})
# # Create your views here.
# # Create your views here.

# def admissionForm(request):
    
#     if request.POST.get('username') and request.POST.get('password') :
#         str=request.POST.get('username')
#         str1=request.POST.get('password')
#         str=str[6:9]
#         #return HttpResponse(str1)
#         if str in board:
#             try:
#                 str=board[str]

#             except():
#                 messages.error(request, 'Credentials not Matched!!')
#                 return redirect('admission_login')


#         str2=request.POST.get('purpose')
#         student=StudentAdmission.objects.filter(ssc_roll=str1,board=str).last()
        
#         if student:
#             if student.status == "Admitted":
#                 messages.error(request, 'Your Admssion already done, you can download admission form!')
#                 return redirect('search_admission_form')
#             try:

#                 context={}
#                 #student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('password'),board=board[str[-3:]],status='Not Admitted').first()
#                 payment_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
#                 group=Group.objects.filter(title_en=student.admission_group).first()
#                 # return HttpResponse(group)
#                 if group:
#                     select_admission=SelectAdmissionForm()
#                     form = StudentForm(instance=student)
#                     subject_form = SubjectChoiceForm(group=group)
#                     adress_formset = AdressFormSet(queryset=Adress.objects.none())
#                     adress_form = AdressForm()
#                     present_adress_form = AdressForm()
#                     ssc_equivalent_form=SscEquvalentForm(instance=student)
#                     guardian_form=GuardianForm()
#                     context={'payment_purpose':payment_purpose,'group':group,'form':form,'subject_form':subject_form,'adress_form':adress_form,'ssc_equivalent_form':ssc_equivalent_form,'guardian_form':guardian_form,'present_adress_form':present_adress_form}
#                     context['adress_formset']=adress_formset
#                     return render(request, 'admission/admission.html',context)      
    
#                 else:
#                     subject_form = None
#                     messages.error(request, 'Group not found!!')
#                     return redirect('admission_login')
#             except():
#                 #print("Exception")
#                 messages.error(request, 'Form creation failed, Try again!!')
#                 return redirect('admission_login')

#     messages.error(request, 'Creadential not matched!!')
#     return redirect('admission_login')


        



# def admissionFormSubmit(request):
    
#     context ={}

#     data = {}
#     flag1=0
#     flag2=0
#     flag3=0
#     if request.method=='POST':
#         # return HttpResponse(request.POST.get('ssc_board'))
#         # student=StudentAdmission.objects.filter(ssc_roll=request.POST.get('ssc_exam_roll'),board=request.POST.get('ssc_board'),status='Not Admitted').first()
#         # return HttpResponse(student)
#         group=None
#         print("got it")
#         student_form=None
#         email=request.POST.get('email')
#         username=request.POST.get('phone')
#         last_name='student'
#         password='Student@'+request.POST.get('phone')
#         student=Student.objects.filter(name=request.POST.get('name'),phone=request.POST.get('phone')).first()
#         ssc_equivalent=SscEquvalent.objects.filter(student=student).first()
#         if UserModel.objects.filter(email=email).exists() is True:
#             email='Email already exist in user system!! '
#             context['email']=email
#             print('1',email,username)
           
#         if UserModel.objects.filter(username=username).exists() is True:
#             phone='Phone number already exist in user system!! '
#             context['phone']=phone
#             print('2',email,username)
            
#         if bool(context):
#             print('5',email,username)
#             return JsonResponse({'context': context},safe=False)
        
#         tran_purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
#         student=Student.objects.filter(name=request.POST.get('name'),phone=request.POST.get('phone')).last()
#         ssc_equivalent=SscEquvalent.objects.filter(student=student).last()
#         if student and ssc_equivalent:
#             student_admission=StudentAdmission.objects.filter(ssc_roll=ssc_equivalent.ssc_exam_roll,name=student.name).first()
#             if  student_admission.status== "Not Admitted":
#                     select_admission=SelectAdmissionForm()
#                     form = StudentForm(instance=student_admission)
#                     subject_form = SubjectChoiceForm(group=student.group)
#                     adress_formset = AdressFormSet(queryset=Adress.objects.none())
#                     adress_form = AdressForm()
#                     present_adress_form = AdressForm()
#                     ssc_equivalent_form=SscEquvalentForm(instance=student_admission)
#                     guardian_form=GuardianForm()
#                     context={'payment_purpose':tran_purpose,'group':student.group,'form':form,'subject_form':subject_form,'adress_form':adress_form,'ssc_equivalent_form':ssc_equivalent_form,'guardian_form':guardian_form,'present_adress_form':present_adress_form}
#                     context['adress_formset']=adress_formset
#                     student.delete()
#                     return render(request, 'admission/admission.html',context)
#                 #return redirect(sslcommerz_payment_gateway_admission(request, student,tran_purpose))
#             else:
#                 messages.error(request, 'Your Admission already done, you can download receipt!')
#                 return redirect('search_admission_form')

#         form = StudentForm(request.POST, request.FILES)
#         ssc_equivalent_form = SscEquvalentForm(request.POST)
#         guardin_form = GuardianForm(request.POST)
#         formset = AdressFormSet(data=request.POST)
#         adress_form = AdressForm(request.POST)
        

#         if form.is_valid():
#             student_form=form.save(commit=False)
#             student_form.gender=request.POST.get('gender')
            
#             group=Group.objects.filter(title_en=request.POST.get('admission_group')).first()
#             student_form.group=group
#             student_form.class_roll=generate_student_id()
#             student_form.std_id=int(student_form.class_roll)
#             session=Session.objects.first()
#             # std_count=Student.objects.filter(group=group,session=session).count()
#             # print(session)
#             # session_string=session.title_en
#             # str1=session_string[-2:]
#             # roll=int(str1)*10000
#             # print(roll)
#             # if group.title_en in 'Science':
#             #     s_roll=roll+1001+std_count
#             #     section=s_roll-roll
#             #     if section<= 1250:
#             #         student_form.section='A'
#             #     elif section> 1250 and section<= 1550:
#             #         student_form.section='B'
#             #     else:
#             #         student_form.section='C'
#             #     print(s_roll)
#             #     student_form.class_roll=str(s_roll)

#             # if group.title_en in 'Humanities':
#             #     s_roll=roll+2001+std_count
#             #     section=s_roll-roll
#             #     if section<= 2250:
#             #         student_form.section='A'
#             #     elif section> 2250 and section<= 2550:
#             #         student_form.section='B'
#             #     else:
#             #         student_form.section='C'
#             #     student_form.class_roll=str(s_roll)
#             # if group.title_en in 'Business Studies':
#             #     s_roll=roll+3001+std_count
#             #     section=s_roll-roll
#             #     student_form.section='A'
               
#             #     student_form.class_roll=str(s_roll)
            
#             if guardin_form.is_valid():
#                 guardin=guardin_form.save()
#                 student_form.guardian_info=guardin
#             if formset.is_valid():
#                 adresses=formset.save()
#                 for index, adress in enumerate(adresses):
#                     adress.save()
#                     if index == 0:
#                         student_form.permanent_adress=adress
#                     else:
#                         student_form.present_adress=adress

#             # if adress_form.is_valid:
#             #     adress=adress_form.save()
#             #     student_form.permanent_adress=adress
                
            
            
#             student_category=StudentCategory.objects.filter(title_en="HSC").first()
#             student_form.student_category=student_category
#             student_form.save()

#             # print('6. Student form',email,username)
#         # print(form.errors)
#         # print(group)
#         subject_form = SubjectChoiceForm(request.POST,group=group)


            
#         if ssc_equivalent_form.is_valid():
#                 ssc_form=ssc_equivalent_form.save(commit=False)
#                 ssc_form.student=student_form
#                 if ssc_form.student:
#                     ssc_form.save()
#         '''if guardin_form.is_valid():
#                 guardian=guardin_form.save(commit=False)
#                 guardian.student=student_form
#                 guardian.save()'''
#         if subject_form.is_valid():
#                 for terminal in subject_form.cleaned_data['compulsory_subject']:
#                     print(terminal)
#                 subject=subject_form.save(commit=False)
#                 subject.student=student_form
#                 compulsory_sub=subject_form.cleaned_data['compulsory_subject']
#                 for i in compulsory_sub:
#                     subject.compulsory_subject.add(i)
#                 if group.title_en not in 'Business Studies':
#                     optional_sub=subject_form.cleaned_data['optional_subject']
#                     for i in optional_sub:
#                         subject.optional_subject.add(i)
#                 else:
#                     subject.optional_subject=None
#                 if subject.student:
#                         subject.save()
                        
#         else: 
            

#         return redirect(sslcommerz_payment_gateway_admission(request, student_form,tran_purpose))
#         # cradentials = {'store_id': 'israb672a4e32dfea5',
#         #     'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
#         # cradentials = {'store_id': 'gmrwcedubdlive',
#         #     'store_pass': '677CD7B61AB5A81511', 'issandbox': False}    
#         # sslcommez = SSLCOMMERZ(cradentials)
#         # body = {}
#         # body['student'] = request.POST.get('name')
#         # body['total_amount'] = 10
#         # body['currency'] = "BDT"
#         # body['tran_id'] = sslcommerz.generator_trangection_id()
#         # body['ipn_url'] = 'https://student.gmrwc.edu.bd/payment/ipn/'
#         # body['fail_url'] = 'https://student.gmrwc.edu.bd/payment/failed/'
#         # body['cancel_url'] = 'https://student.gmrwc.edu.bd/payment/canceled/'
#         # body['success_url'] = 'https://student.gmrwc.edu.bd/payment/success/'
#         # body['emi_option'] = 0
#         # body['cus_name'] = request.POST.get('name')
#         # body['cus_email'] = 'request.data["email"]'
#         # body['cus_phone'] = request.POST.get('phone')
#         # body['cus_add1'] = 'request.data["address"]'
#         # body['cus_city'] = 'request.data["address"]'
#         # body['cus_country'] = 'Bangladesh'
#         # body['shipping_method'] = "NO"
#         # body['multi_card_name'] = ""
#         # body['num_of_item'] = 1
#         # body['product_name'] = "Test"
#         # body['product_category'] = "Test Category"
#         # body['product_profile'] = "general"
#         # body['value_a'] = student_form.class_roll
#         # body['value_b'] = student_form.name
#         # body['value_c'] = student_form.phone
#         # body['value_d'] = 1          
#         # response = sslcommez.createSession(body)
      


#         # #return redirect["GatewayPageURL"]

#         # return redirect('https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"])

# def formDownload(request):
#         phone=request.POST.get('student_id')
#         student=Student.objects.filter(phone=phone).first()
#         subject_choice=SubjectChoice.objects.filter(student=student).first()
        
#         ssc_equivalent=SscEquvalent.objects.filter(student=student).first()


#         return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice})

# def SubprocessesView(request):
#         if request.POST.get('id') == 'id_form-0-division':
#             division=Division.objects.filter(id=request.POST.get('value')).first()
#             district=District.objects.filter(division=division)
#             district=list(district.values())
#         if request.POST.get('id') == 'id_form-1-division':
#             division=Division.objects.filter(id=request.POST.get('value')).first()
#             district=District.objects.filter(division=division)
#             district=list(district.values())

#         if request.POST.get('id') == 'id_form-0-district':
#             division=District.objects.filter(id=request.POST.get('value')).first()
#             upazilla=Upazilla.objects.filter(district=division)
#             district=list(upazilla.values())
#         if request.POST.get('id') == 'id_form-1-district':
#             division=District.objects.filter(id=request.POST.get('value')).first()
#             upazilla=Upazilla.objects.filter(district=division)
#             district=list(upazilla.values())

#         return JsonResponse({'status':'success','meaasge':'Account created Successfully','district':district},safe=False)

# class SearchAdmissionView(View):
#     template_name = 'admission/search_admission_form.html'
    
#     def get(self, request, *args, **kwargs):
#         context={}
#         form=SearchAdmissionForm()
#         context['form'] = form
#         return render(request, self.template_name,context)

#     def post(self, request, *args, **kwargs):
#         context={}
#         roll=request.POST.get('roll').strip()
#         student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).last()
#         if student is None:
#             form=SearchAdmissionForm()
#             context['notfound']="Student Not Found, Please complete admission proccess!"
#             context['form'] = form
#             return render(request, self.template_name,context)
#         subject_choice=SubjectChoice.objects.filter(student=student).first()
#         ssc_equivalent=SscEquvalent.objects.filter(student=student).first()
#         return render(request, 'admission/admission_dummy.html',{'student':student,'ssc_equivalent':ssc_equivalent,'subject_choice':subject_choice})
        
# class IDCardView(View):
#     template_name = 'admission/get_id_card.html'
    
#     def get(self, request, *args, **kwargs):
#         context={}
#         form=SearchIDCardForm()
#         context['form'] = form
#         return render(request, self.template_name,context)

#     def post(self, request, *args, **kwargs):
#         context={}
#         roll_from=request.POST.get('roll_from').strip()
#         roll_to=request.POST.get('roll_to').strip()
#         group=request.POST.get('group').strip()
#         session=request.POST.get('session').strip()
#         student1=Student.objects.filter(class_roll=request.POST.get('roll_from').strip()).last()
#         student2=Student.objects.filter(class_roll=request.POST.get('roll_to').strip()).last()
#         students=None
#         if student1 and student2:
#             students=Student.objects.filter(id__range=(student1.id,student2.id),session=session,group=group)
#         if students is None:
#             form=SearchIDCardForm()
#             context['notfound']="Student Not Found, Please complete admission proccess!"
#             context['form'] = form
#             return render(request, self.template_name,context)
#         context['students'] = students
#         context['session'] = "form"
#         context['form'] = "form"


#         return render(request, 'admission/student_id_card.html',context)

