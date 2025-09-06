from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchPaymentForm,SearchPaymentReceiptForm
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views.generic import View, TemplateView, DetailView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpResponseNotFound
from .models import Transaction,PaymentPurpose,PaymentType, PaymentConsession,PaymentGateway
from student.models import Student,GuardianInfo,SscEquvalent,SubjectChoice,Session,Choice
from admission.models import StudentAdmission
from .sslcommerz import sslcommerz_payment_gateway
from sslcommerz_lib import SSLCOMMERZ 
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import Q
import os
from django.conf import settings

# Create your views here.
# cradentials = {'store_id': 'israb672a4e32dfea5',
#             'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True}
# cradentials = {'store_id': 'gmrwcedubdlive',
#             'store_pass': '677CD7B61AB5A81511', 'issandbox': False}
gateway = PaymentGateway.objects.filter(is_active=True).first()
cradentials = {'store_id': gateway.store_id,
            'store_pass': gateway.store_pass, 'issandbox': gateway.is_sandbox}
  
sslcommez = SSLCOMMERZ(cradentials)

class Index(TemplateView):
    template_name = "payment/index.html"

def DonateView(request):
    name = request.POST['name']
    amount = request.POST['amount']
    return redirect(sslcommerz_payment_gateway(request, name, amount))

def PaymentView(request,student,name,amount):
    name = request.POST['name']
    amount = request.POST['amount']
    return redirect(sslcommerz_payment_gateway(request, name, amount))


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutSuccessView(View):
    model = Transaction
    template_name = 'payment/payment_receipt.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('nothing to see')

    def post(self, request, *args, **kwargs):
        
        context={}
        data = self.request.POST
        #print(data)

        
        #print(tran_purpose.payment_type.id)
        transaction=Transaction.objects.filter(val_id=data['val_id']).first()
        #tran_type=PaymentType.objects.filter(id=data['value_d']).first()
        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).last()
        student=Student.objects.filter(Q(class_roll=data['value_a']) | Q(std_id=data['value_a'])).first()
        # return HttpResponse(student)
        context['tran_purpose']=tran_purpose
        
        transaction=None

        if tran_purpose.payment_type.id == 2:
                #print("data['value_d']:",tran_purpose.payment_type)
                #print(student)
                context['transaction']=transaction
                context['purpose']=tran_purpose
                context['student']=student
                return render(request,self.template_name,context)
        if tran_purpose.payment_type.id == 3:
                #print("data['value_d']:",tran_purpose.payment_type)
                #print(student)
                context['transaction']=transaction
                context['purpose']=tran_purpose
                context['student']=student
                return render(request,self.template_name,context)

        if tran_purpose.payment_type.id == 1:
                
                subject_choice=SubjectChoice.objects.filter(student=student).first()
                subject_choices=[]
                for subject in subject_choice.compulsory_subject.all():
                    subject_choices.append(subject)
                for subject in subject_choice.optional_subject.all():
                    subject_choices.append(subject)
                
                ssc_equivalent=SscEquvalent.objects.filter(student=student).first()
                
                # password="Student@"+data['value_c']
                # user = get_user_model.objects.create_user(username=data['value_c'],
                #                  email=data['value_c'],last_name="Student",
                #                  password=password,is_active=False)
                # student.user=user
                # student.save()
                # students=Student.objects.filter(phone=data['value_b'],user=None)
                # for std in students:
                #     std.delete()

                context['purpose']=tran_purpose
                context['student']=student
                context['ssc_equivalent']=ssc_equivalent
                context['subject_choice']=subject_choice
                context['subject_choices']=subject_choices
                return render(request,'admission/admission_form.html',context)
        return render(request,self.template_name,context)


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutIPNView(View):
    model = Transaction
    template_name = 'payment/payment_receipt.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('nothing to see')

    def post(self, request, *args, **kwargs):
        
        context={}
        data = self.request.POST
        post_body={}
        # print(data)
        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).first()
        student=Student.objects.filter(Q(class_roll=data['value_a']) | Q(std_id=data['value_a'])).last()
        # ssc_equivalent=SscEquvalent.objects.filter

        if data['status'] == 'VALID':
            if tran_purpose.payment_type.id == 1:
                subject_choice=SubjectChoice.objects.filter(student=student).first()
                ssc_equivalent=SscEquvalent.objects.filter(student=student).first()
                student_admission=StudentAdmission.objects.filter(ssc_roll=ssc_equivalent.ssc_exam_roll,board=ssc_equivalent.ssc_board).last()
                session=student_admission.admission_session
                std_count=Student.objects.filter(group=student.group,session=session,is_active=True).count()
                session_string=session.title_en
                str1=session_string[-5:-3]
                roll=int(str1)*10000
                #print(roll)
                if student.group.title_en in 'Science':
                    s_roll=roll+1001+std_count
                    section=s_roll-roll
                    if section<= 1250:
                        student.section='A'
                    elif section> 1250 and section<= 1550:
                        student.section='B'
                    else:
                        student.section='C'
                    print(s_roll)
                    student.class_roll=str(s_roll)

                if student.group.title_en in 'Humanities':
                    s_roll=roll+2001+std_count
                    section=s_roll-roll
                    if section<= 2250:
                        student.section='A'
                    elif section> 2250 and section<= 2550:
                        student.section='B'
                    else:
                        student.section='C'
                    student.class_roll=str(s_roll)
                if student.group.title_en in 'Business Studies':
                    s_roll=roll+3001+std_count
                    section=s_roll-roll
                    student.section='A'
                
                    student.class_roll=str(s_roll)
                student.save()
                old_path=student.image.path
                ext = student.image.name.split('.')[-1]
                filename = str(student.class_roll)+'.'+ext
                year=str(datetime.now().year)
                student.image.name = os.path.join('media/student/'+year,filename)
                student.is_active=True
                student.save()
                student.guardian_info.serial=int(student.class_roll)
                student.guardian_info.save()
                new_path = os.path.join(settings.MEDIA_ROOT, 'media/student/'+year, filename)
                if old_path:
                    os.rename(old_path, new_path)
                subject_choice.class_roll=student.class_roll
                subject_choice.save()
                choice=Choice.objects.filter(class_roll=student.class_roll).last()
                if choice is None:
                    subjects=set()
                    for subject in subject_choice.compulsory_subject.all():
                            subjects.add(subject)
                    for subject in subject_choice.optional_subject.all():
                            subjects.add(subject)
                    subjects=list(subjects)
                    choice=Choice.objects.create(class_roll=student.class_roll, name=student.name, subject1=subjects[0], subject2=subjects[1], subject3=subjects[2], subject4=subjects[3], subject5=subjects[4], subject6=subjects[5], fourth_subject=subject_choice.fourth_subject, group=student.group,session=student.session)  
                student_admission.status="Admitted"
                student_admission.save()
            post_body['val_id'] = data['val_id']
            response = sslcommez.validationTransactionOrder(post_body['val_id'])
            transaction=Transaction.objects.create(
                            class_roll=student.class_roll,
                            name = student.name,
                            group=student.group,
                            session=student.session,
                            department=student.department,
                            phone=data['value_c'],
                            email=data['value_c'],
                            tran_id=data['tran_id'],
                            tran_purpose=tran_purpose,
                            val_id=data['val_id'],
                            amount=data['amount'],
                            card_type=data['card_type'],
                            card_no=data['card_no'],
                            store_amount=data['store_amount'],
                            bank_tran_id=data['bank_tran_id'],
                            status=data['status'],
                            tran_date=data['tran_date'],
                            currency=data['currency'],
                            card_issuer=data['card_issuer'],
                            card_brand=data['card_brand'],
                            card_issuer_country=data['card_issuer_country'],
                            card_issuer_country_code=data['card_issuer_country_code'],
                            verify_sign=data['verify_sign'],
                            verify_sign_sha2=data['verify_sign_sha2'],
                            currency_rate=data['currency_rate'],
                            risk_title=data['risk_title'],
                            risk_level=data['risk_level'],
            
                        )
        else:
            transaction=Transaction.objects.create(
                            class_roll=data['value_a'],
                            name = data['value_b'],
                            group=student.group,
                            session=student.session,
                            department=student.department,
                            phone=data['value_c'],
                            email=data['value_c'],
                            tran_id=data['tran_id'],
                            tran_purpose=tran_purpose,
                            val_id="None",
                            amount=data['amount'],
                            card_type=data['card_type'],
                            card_no=data['card_no'],
                            store_amount=0,
                            bank_tran_id=data['bank_tran_id'],
                            status=data['status'],
                            tran_date=data['tran_date'],
                            currency=data['currency'],
                            card_issuer=data['card_issuer'],
                            card_brand=data['card_brand'],
                            card_issuer_country=data['card_issuer_country'],
                            card_issuer_country_code=data['card_issuer_country_code'],
                            verify_sign=data['verify_sign'],
                            verify_sign_sha2=data['verify_sign_sha2'],
                            currency_rate=data['currency_rate'],
                            risk_title='None',
                            risk_level='0',
            
                        )            # if response['status']== 'VALID' or response['status']== 'VALIDATED' or response['status'] == 'INVALID_TRANSACTION':
        
        messages.success(request,'Something Went Wrong')
        context['messages']=messages
        # print('IPN Hit Exeption: ',data)
        return redirect('/')



@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFaildView(View):
    template_name = 'payment/failed.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data=request.POST
        context={}
        student=Student.objects.filter(Q(class_roll=data['value_a']) | Q(std_id=data['value_a'])).first()
        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).first()
        context['tran_purpose']=tran_purpose
        if tran_purpose.payment_type.id == 1:
            if student:
                if student.image:  # Check if an image exists
                    image = student.image.path
                    if os.path.exists(image):
                        os.remove(image)
                student.delete()
        return render(request,self.template_name,context)

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutCanceledView(View):
    template_name = 'payment/canceled.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data=request.POST
        context={}
        student=Student.objects.filter(Q(class_roll=data['value_a']) | Q(std_id=data['value_a'])).first()
        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).first()
        context['tran_purpose']=tran_purpose
        if tran_purpose.payment_type.id == 1:
            if student:
                if student.image:  # Check if an image exists
                    image = student.image.path
                    if os.path.exists(image):
                        os.remove(image)
                student.delete()        
        messages.success(request,'Payment Canceled')
        context['messages']=messages
        return render(request,self.template_name,context)

def searchPayment(request):
    context={}
    flag1=0
    flag2=0
    
    if request.method=='POST':
        
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        subject_choice=Choice.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        transaction=Transaction.objects.filter(class_roll=request.POST.get('roll').strip(),status="VALID", tran_purpose=purpose).first()
        if transaction:
            context['notfound']="You already paid for "+ purpose.title_en +", You can download your receipt from 'https://student.gmrwc.edu.bd/payment/get_payment_receipt/' "
        elif student:
            #print(student,purpose)
            payment_consession=PaymentConsession.objects.filter(class_roll=request.POST.get('roll').strip(), group=student.group, department=student.department,tran_purpose=purpose).last()
            context['student']=student
            context['purpose']=purpose
            context['payment_consession']=payment_consession

            #return render(request, 'payment/search_payment.html', context=context)

            return render(request, 'payment/check_payment_info.html', context=context)

        else:
            context['notfound']="Student not found!! Re=Enter Right Information or Contact  control room"
        
    form=SearchPaymentForm(instance=request.user)
    context['form']=form
    return render(request, 'payment/search_payment.html', context=context)


def ProceedPayment(request):
    context={}

    if request.method=='POST':

        student=Student.objects.filter(class_roll=request.POST.get('student')).first()

        subject_choice=Choice.objects.filter(class_roll=request.POST.get('student')).first()
        purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        transaction=Transaction.objects.filter(class_roll=request.POST.get('roll'),status="VALID", tran_purpose=purpose).first()
        if transaction:
            context['notfound']="You already paid for "+ purpose.title_en +", You can download your receipt from 'https://student.gmrwc.edu.bd/payment/get_payment_receipt/' "
            form=SearchPaymentForm(instance=request.user)
            context['form']=form
            return render(request, 'payment/search_payment.html', context=context)
        if student:
            return redirect(sslcommerz_payment_gateway(request, student, purpose))

        
        
    form=SearchPaymentForm(instance=request.user)
    context['form']=form
    return render(request, 'payment/search_payment.html', context=context)

def getPaymentReceipt(request):
    context={}
    flag1=0
    flag2=0
    
    if request.method=='POST':
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        subject_choice=Choice.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose')).first()
        transaction=Transaction.objects.filter(class_roll=request.POST.get('roll').strip(),tran_purpose=purpose,status="VALID").last()
        if student and transaction:
            context['student']=student
            context['purpose']=purpose
            return render(request, 'payment/payment_receipt.html', context=context)
        else:
            context['notfound']="Student or transaction not found!!\n Re=Enter Right Information or Contact  control room"    
    
    form=SearchPaymentReceiptForm(instance=request.user)
    context['form']=form
    return render(request, 'payment/search_payment_receipt.html', context=context)

