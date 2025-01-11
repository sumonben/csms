from django.http import HttpResponse
from django.shortcuts import render
from student.models import Student , Choice
from .forms import SearchPaymentForm
from .models import PaymentPurpose
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views.generic import View, TemplateView, DetailView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpResponseNotFound
from .models import Transaction,PaymentPurpose
from student.models import Student,GuardianInfo,SscEquvalent,SubjectChoice
from .sslcommerz import sslcommerz_payment_gateway
from sslcommerz_lib import SSLCOMMERZ 
from django.contrib.auth import get_user_model

# Create your views here.
cradentials = {'store_id': 'israb672a4e32dfea5',
            'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
            
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

        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).first()
        student=Student.objects.filter(class_roll=data['value_a']).first()
        context['tran_purpose']=tran_purpose
        #print(tran_purpose.payment_type.id)
        transaction=None
        try:
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
            #print("data['value_d']:",tran_purpose.payment_type)
            
            if tran_purpose.payment_type.id == 2:
                #print("data['value_d']:",tran_purpose.payment_type)
                student=Student.objects.filter(class_roll=data['value_a']).first()
                #print(student)
                context['transaction']=transaction
                context['purpose']=tran_purpose
                context['student']=student
                return render(request,self.template_name,context)
            if tran_purpose.payment_type.id == 3:
                #print("data['value_d']:",tran_purpose.payment_type)
                student=Student.objects.filter(class_roll=data['value_a']).first()
                #print(student)
                context['transaction']=transaction
                context['purpose']=tran_purpose
                context['student']=student
                return render(request,self.template_name,context)

            if tran_purpose.payment_type.id == 1:
                student=Student.objects.filter(phone=data['value_b']).last()
                password="Student@"+data['value_c']
                user = get_user_model.objects.create_user(username=data['value_c'],
                                 email=data['value_c'],last_name="Student",
                                 password=password,is_active=False)
                student.user=user
                student.save()
                students=Student.objects.filter(phone=data['value_b'],user=None)
                for std in students:
                    std.delete()

                #print(student)
                context['purpose']=tran_purpose
                context['student']=student
            messages.success(request,'Payment Successful!!')
            
        except:
            messages.success(request,'Something Went Wrong')
            context['messages']=messages
        return render(request,self.template_name,context)




@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFaildView(View):
    template_name = 'payment/failed.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data=request.POST
        context={}
        tran_purpose=PaymentPurpose.objects.filter(id=data['value_d']).first()
        context['tran_purpose']=tran_purpose
        
        if data['value_d'] == '1':
            certificate=Certificate.objects.filter(phone=data['value_b'],transaction=None)
            if certificate:
                certificate.delete()
        if data['value_d'] == '2':
            student=Student.objects.filter(phone=data['value_b']).first()
            #user=UserModel.objects.filter(username=data['value_b']).first()
            #user.delete()

        '''certificate=Certificate.objects.filter(transaction=None)
        print(request.POST)
        
        for cert in certificate:
            response = sslcommez.transaction_query_session(cert.session_key)
            print(response['status'])
            print(response)

            if response['status'] in 'FAILED' or response['status'] in 'PENDING':
                cert.delete()'''
        return render(request, self.template_name,context)

def searchPayment(request):
    context={}
    flag1=0
    flag2=0
    
    if request.method=='POST':
        
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        subject_choice=Choice.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose'),is_active=True).first()
        if student:
            #print(student,purpose)

            context['student']=student
            context['purpose']=purpose
            
            #return render(request, 'payment/search_payment.html', context=context)

            return render(request, 'payment/check_payment_info.html', context=context)

        
        
    form=SearchPaymentForm()
    context['form']=form
    return render(request, 'payment/search_payment.html', context=context)


def ProceedPayment(request):
    context={}

    if request.method=='POST':

        student=Student.objects.filter(class_roll=request.POST.get('student')).first()

        subject_choice=Choice.objects.filter(class_roll=request.POST.get('student')).first()
        purpose=PaymentPurpose.objects.filter(id=request.POST.get('purpose'),is_active=True).first()
        if student:
            return redirect(sslcommerz_payment_gateway(request, student, purpose))

        
        
    form=SearchPaymentForm()
    context['form']=form
    return render(request, 'payment/search_payment.html', context=context)
