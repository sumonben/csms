import string
import random
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateway


def generator_trangection_id( size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


    

def sslcommerz_payment_gateway(request, student,purpose):
    
    print(student,purpose)
    gateway = PaymentGateway.objects.all().first()
    cradentials = {'store_id': 'israb672a4e32dfea5',
            'store_pass': 'israb672a4e32dfea5@ssl', 'issandbox': True} 
    
    cradentials = {'store_id': 'gmrwcedubdlive',
            'store_pass': '677CD7B61AB5A81511', 'issandbox': False} 
    
    sslcommez = SSLCOMMERZ(cradentials)
    body = {}
    body['student'] = student
    body['total_amount'] = purpose.amount
    body['currency'] = "BDT"
    body['tran_id'] = generator_trangection_id()
    body['success_url'] = 'http://localhost:8000/payment/success/'
    body['fail_url'] = 'http://localhost:8000/payment/payment/failed/'
    body['cancel_url'] = 'http://localhost:8000/payment/canceled/'
    body['emi_option'] = 0
    body['cus_name'] = student.name
    body['cus_email'] = 'request.data["email"]'
    if student.phone:
        body['cus_phone'] = student.phone
    else:
        body['cus_phone'] = '01712539569'
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
    print(response)   
    return  response["GatewayPageURL"]
    return 'https://securepay.sslcommerz.com/gwprocess/v4/api.php?Q=pay&SESSIONKEY=' + response["sessionkey"]

