import string
import random
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateway, PaymentConsession
import uuid

# cradentials = {'store_id': 'israb672a4e32dfea5',
#             'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
    
# cradentials = {'store_id': 'gmrwcedubdlive',
#             'store_pass': '677CD7B61AB5A81511', 'issandbox': False} 
            
# def generator_trangection_id( size=8, chars=string.ascii_uppercase + string.digits):
#     return "".join(random.choice(chars) for _ in range(size))
gateway = PaymentGateway.objects.filter(is_active=True).first()
cradentials = {'store_id': gateway.store_id,
            'store_pass': gateway.store_pass, 'issandbox': gateway.is_sandbox}
def generate_transaction_id():
    return uuid.uuid4().hex

    

def sslcommerz_payment_gateway(request, student,purpose):
    
    #print(student,purpose)
     
    payment_consession=PaymentConsession.objects.filter(class_roll=student.class_roll, group=student.group, department=student.department,tran_purpose=purpose).last()

    sslcommez = SSLCOMMERZ(cradentials)
    body = {}
    body['student'] = student
    if payment_consession:
        body['total_amount'] = payment_consession.amount
    else:
        if student.group.title_en == 'Science':
            body['total_amount'] = purpose.amount_science
        if student.group.title_en == 'Humanities':
            body['total_amount'] = purpose.amount_humanities
        if student.group.title_en == 'Business Studies':
            body['total_amount'] = purpose.amount_bussiness
    body['currency'] = "BDT"
    body['tran_id'] = generate_transaction_id()
    body['ipn_url'] = 'https://student.gmrbwc.edu.bd/payment/ipn/'
    body['fail_url'] = 'https://student.gmrbwc.edu.bd/payment/failed/'
    body['cancel_url'] = 'https://student.gmrbwc.edu.bd/payment/canceled/'
    body['success_url'] = 'https://student.gmrbwc.edu.bd/payment/success/'
    #body['success_url'] ='https://' +str(request.META['HTTP_HOST'])+'/payment/success/'
    # body['fail_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/failed/'
    # body['cancel_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/canceled/'
    # body['ipn_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/ipn/'
    body['emi_option'] = 0
    body['cus_name'] = student.name
    body['cus_email'] = 'request.data["email"]'
    if student.phone:
        body['cus_phone'] = student.phone
    else:
        body['cus_phone'] = '01309119250'
    body['cus_add1'] = 'request.data["address"]'
    body['cus_city'] = 'request.data["address"]'
    body['cus_country'] = 'Bangladesh'
    body['shipping_method'] = "NO"
    body['multi_card_name'] = ""
    body['num_of_item'] = 1
    body['product_name'] = "Test"
    body['product_category'] = "Test Category"
    body['product_profile'] = "general"
    body['value_a'] = student.class_roll
    body['value_b'] = student.name
    body['value_c'] = student.phone
    body['value_d'] = purpose.id

    


    response = sslcommez.createSession(body)
    #print(response)   
    return  response["GatewayPageURL"]
    return 'https://securepay.sslcommerz.com/gwprocess/v4/api.php?Q=pay&SESSIONKEY=' + response["sessionkey"]

# cradentials = {'store_id': 'israb672a4e32dfea5',
#             'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
    
# cradentials = {'store_id': 'gmrwcedubdlive',
#             'store_pass': '677CD7B61AB5A81511', 'issandbox': False}
def sslcommerz_payment_gateway_admission(request, student,purpose):
        sslcommerz = SSLCOMMERZ(cradentials)
        body = {}
        body['student'] = student.name
        if student.group.title_en == 'Science':
            body['total_amount'] = purpose.amount_science
        if student.group.title_en == 'Humanities':
            body['total_amount'] = purpose.amount_humanities
        if student.group.title_en == 'Business Studies':
            body['total_amount'] = purpose.amount_bussiness
        body['currency'] = "BDT"
        body['tran_id'] = generate_transaction_id()
        # body['ipn_url'] = 'https://student.gmrwc.edu.bd/payment/ipn/'
        # body['fail_url'] = 'https://student.gmrwc.edu.bd/payment/failed/'
        # body['cancel_url'] = 'https://student.gmrwc.edu.bd/payment/canceled/'
        # body['success_url'] = 'https://student.gmrwc.edu.bd/payment/success/'
        body['success_url'] ='https://' +str(request.META['HTTP_HOST'])+'/payment/success/'
        body['fail_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/failed/'
        body['cancel_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/canceled/'
        body['ipn_url'] = 'https://' +str(request.META['HTTP_HOST'])+'/payment/ipn/'
        body['emi_option'] = 0
        body['cus_name'] = student.name
        body['cus_email'] = 'request.data["email"]'
        body['cus_phone'] = student.phone
        body['cus_add1'] = 'request.data["address"]'
        body['cus_city'] = 'request.data["address"]'
        body['cus_country'] = 'Bangladesh'
        body['shipping_method'] = "NO"
        body['multi_card_name'] = ""
        body['num_of_item'] = 1
        body['product_name'] = "Test"
        body['product_category'] = "Test Category"
        body['product_profile'] = "general"
        body['value_a'] = student.class_roll
        body['value_b'] = student.name
        body['value_c'] = student.phone
        body['value_d'] = purpose.id         
        response = sslcommerz.createSession(body)
        print(response["sessionkey"])   

        return  response["GatewayPageURL"]
        return 'https://securepay.sslcommerz.com/gwprocess/v4/api.php?Q=pay&SESSIONKEY=' + response["sessionkey"]

