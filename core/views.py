# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import random
from cryptography.fernet import Fernet
import re
import yaml
import coreapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.template.loader import get_template
from django.core.mail import EmailMessage
import uuid
import datetime
import authorize
from django.contrib.auth.models import User
import string
from core.models import *
from rfp.models import *
from rfp.models import Subscribers, UnsubscriberQuery
from user_payment.models import Payment,PaymentLogs,PaymentCardInfo
from django.utils import timezone
from core.backgroundtasks import notify_user,notify_user1,notify_user2,notify_user3
from core.serializers import *
from rest_framework.permissions import IsAuthenticated

import requests
import json
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER






@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        obj = request.data['obj']
        # print(obj)
        first_name = obj['firstname']
        last_name = obj['lastname']
        company = obj['companyname']
        email = obj['email']
        username = obj['username']
        password = obj['password']
        # phone_no = obj['phone']
        address = obj['address']
        zipcode = obj['zipcode']
        city = obj['city']
        country = obj['country']
        state = obj['state']
        phone_no = obj['phone']

        # print (username)
        # print  (password)
        # user = User.
        user = User.objects.create_user(username = username, email = email,password= password, first_name = first_name, last_name= last_name)
        # user.save()
        register = Register(user=user,company=company,address=address,zipcode=zipcode,city=city,country=country,state=state,phone_no=phone_no)
        register.save()
        #sendSubscription1(email)
        return Response({'msg': 'User Registered Successfully' }, status=status.HTTP_200_OK)



@api_view(['GET'])
def zip_data(request , zipcode):
    client = coreapi.Client()
    #response = client.get('http://www.zipcodeapi.com/rest/p5diD53qnvX1nSFIaXQAP8VRiJzwYKmoPzGsFKT2fQ4DIJlTHbuwkpnC8X97Hwwx/info.json/'+zipcode+'/radians')

    url = ('http://ziptasticapi.com/'+zipcode)
    response=requests.get(url)
    data=response.json()
    data={'country':data['country'],
          'city':data['city'],
          'state':data['state']}
    return Response(data)

def sendSubscription1(email  ):
    # if request.method == 'POST':
        try:
            # user1 = User.objects.filter(email=request.data['email'])
            # if user1.exists() == False :
                user = Subscribers.objects.filter(email=email)
                if user.exists() == False:
                # print("Email Dictionary " , dictionary)
                # key = {{'title': ' Exterior Surface Cleaning Services ', 'State': 'North Carolina', 'category': 'Cleaning, Janitorial and Custodial Services and Supplies', 'link': 'https://www.rfpmart.com/84293-usa-charlotte-north-carolina-exterior-surface-cleaning-services-rfp.html'}, {'title': ' Security Camera System, Access Control Door System and Key Card Printer Maintenance Services ', 'State': 'California', 'category': 'CCTV and Security Services and Supplies', 'link': 'https://www.rfpmart.com/84292-usa-sacramento-california-security-camera-system-access-control-door-system-and-key-card-printer-maintenance-services-rfp.html'}, {'title': ' Strategic Planning Services ', 'State': 'California', 'category': 'Cleaning, Janitorial and Custodial Services and Supplies', 'link': 'https://www.rfpmart.com/84291-usa-california-strategic-planning-services-rfp.html'}}
                    em = email
                    sp = re.split(r'[0-1|.|_|-]', em)
                    key = {
                        'dic': sp[0].upper(),
                        'email': em
                    }

                    # email_list = ['ali.raza@brainplow.com', 'jonybutt3@gmail.com']
                    email_list = []
                    email_list.append(email)

                    print("Email ", email_list)

                    message = get_template('RFPGurus-Subscription.html').render(key)
                    email = EmailMessage('Your Subscription Alert', message, to=email_list)
                    email.content_subtype = 'html'
                    email.send()
                    Subscribers.objects.get_or_create(email=email)
                    return True
        except:
            return False


@api_view(['PUT','GET'])
#@permission_classes((IsAuthenticated,))
def Users_details_update(request,username):
    # current_user = request.user
    # print(request.method)
    try:
        user = User.objects.get(username= username)
        profile = Register.objects.get(user=user)
    except Register.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        # serializer1 = Register1Serializer(profile , data=request.data)
        # serializer = Register1Serializer(profile , data=request.data)
        # if serializer.is_valid():
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.username = request.data['username']
            user.save()
            print("Saved")
            print (request.data['newsletter'])
            profile.company = request.data['company']
            profile.address = request.data['address']
            profile.zipcode = request.data['zipcode']
            profile.city = request.data['city']
            profile.country = request.data['country']
            profile.state = request.data['state']
            profile.phone_no = request.data['phone']
            profile.newsletter = request.data['newsletter']
            if 'usercat' in request.data:
                profile.user_preference = request.data['usercat']
            if 'prefersate' in request.data:
                profile.state_preference = request.data['prefersate']
            if 'preferagency' in request.data:
                profile.agency_preference = request.data['preferagency']
            if 'prefercities' in request.data:
                profile.city_preference = request.data['prefercities']
            if 'prefercounty' in request.data:
                profile.county_preference = request.data['prefercounty']

            profile.save()
            print(request.data)
            return Response(request.data)
    elif request.method == 'GET':
        serializer = Register1Serializer(profile)
        return Response(serializer.data)



@api_view(['POST'])
def authenticated_login(request):
    if request.method == 'POST':
        username = request.data['username']
        user = User.objects.get(username=username)
        reg_obj = Register.objects.get(user=user)
        if reg_obj.is_subscribed == True:
            print("in subscription")
            date1 = datetime.datetime.now()
            date = str(date1)[0:10]
            auto = False
            card = PaymentCardInfo.objects.filter(user=user)
            for c in card:
                if c.autopay == True:
                    auto = True
                    print("auto pay", auto)

            if auto == False:

                exp = Payment.objects.filter(reg_fk=reg_obj)
                for i in exp:
                    if (i.is_expired == False):
                        if (date >= str(i.end_date)):
                            print("expired change values")
                            i.is_expired = True
                            i.save()
                            reg_obj.is_subscribed = False
                            reg_obj.save()
                            key = {
                                "name": user.username
                            }
                            message = get_template('rfp-gurus-Package_Expiration.html').render(key)
                            email = EmailMessage('Subscription Package is Expired', message, to=[user.email])
                            email.content_subtype = 'html'
                            email.send()

                            print("mail sent")
                        else:
                            pass
                    else:
                        print
            else:
                pass

        if (reg_obj.is_authenticated == True):


            #LoggedInUser.objects.create_or_update(session_key=request.session.session_key, user=request.user)
            return Response({'msg': 'Authenticated User'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'UnAuthnticated User'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_activation_code(request):
    if request.method == 'POST':
        print('activation')
        email = request.data['email']
        user = User.objects.get(email=email)
        register_obj = Register.objects.get(user=user)
        secret_id = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _
            in range(100))

        while (Register.objects.filter(authenticate_code=secret_id).exists()):
            secret_id = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                for _ in
                range(100))

        key = {
            'link': 'https://www.rfpgurus.com/activateaccount/' + secret_id,
            'name':user.username

        }

        message = get_template('rfp-gurus-activation.html').render(key)
        print(user.email)
        email = EmailMessage('Email Confirmation', message, to=[email])
        email.content_subtype = 'html'
        email.send()
        register_obj.authenticate_code = secret_id
        register_obj.save()
        return Response({'msg': 'Email Send'}, status=status.HTTP_200_OK)


        # if request.method == 'PUT':
        #     print('activation')
        #     if True:
        #         email = request.data['email']
        #         # email = "junaid.amjad@brainplow.com"
        #         user = User.objects.filter(email=email).first()
        #         register_obj = Register.objects.get(user=user)
        #         print('////////////////////////////////////', user.first_name)
        #     else:
        #         return Response({'message': 'Incorrect Email'}, status=status.HTTP_400_BAD_REQUEST)
        #     ch = True
        #     while (ch):
        #         try:
        #             secret_id = random.randint(100000, 999999)
        #             register_obj.authentication_code = secret_id
        #             register_obj.save()
        #             ch = False
        #         except:
        #             ch = True
        #
        #     key = {
        #         'link': secret_id
        #     }
        #
        #     message = get_template('email_verification.html').render(key)
        #     email = EmailMessage('Email Confirmation', message, to=[email])
        #     email.content_subtype = 'html'
        #     email.send()
        #
        #     return Response({'message': 'Email Send'}, status=status.HTTP_200_OK)

@api_view (['GET'])
def activate_account(request,uid):
    if request.method == 'GET':
        try:
            if (Register.objects.filter(authenticate_code=uid).exists()):
                reg = Register.objects.get(authenticate_code=uid)
                reg.is_authenticated=True
                reg.newsletter = True
                reg.save()
                return Response({'Msg': 'Account Activated'}, status=status.HTTP_200_OK)

            else:
                return Response({'Msg': 'Error '}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Msg': 'Error '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forget_password(request):
    if request.method == 'POST':
        email = request.data['email']
        user = User.objects.get(email=email)
        reg_obj = Register.objects.get(user=user)
        if(reg_obj.is_authenticated == True):
            reset_email = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(200))
            while (Register.objects.filter(authenticate_code=reset_email).exists()):
                reset_email = ''.join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _
                    in
                    range(100))
            key = {
                'link': 'https://www.rfpgurus.com/forgetpassword/'+reset_email,
                'name':user.username
            }
            message = get_template('rfp-gurus-reset-password.html').render(key)
            email = EmailMessage('Email Confirmation', message, to=[email])
            email.content_subtype = 'html'
            email.send()
            reg_obj.authenticate_code = reset_email
            reg_obj.save()
            return Response({'msg': 'Reset Email Send'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'UnAuthnticated User'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def sendMarketing(request  ):
    if request.method == 'POST':
            try:
                user = Subscribers.objects.filter(email=request.data['email'])
                if user.exists() == False:
                    user = User.objects.filter(email=request.data['email'])
                if user.exists():
                    key = {
                        'name': request.data['email']
                    }
                    # email_list = ['ali.raza@brainplow.com', 'jonybutt3@gmail.com']
                    email_list = []
                    email_list.append(request.data['email'])
                    print("Email ", email_list)
                    # if user.exists():
                    message = get_template('RFPGurus-Marketing.html').render(key)
                    email = EmailMessage('Marketing', message, to=email_list)
                    email.content_subtype = 'html'
                    email.send()
                    return Response({'msg':"Marketing Alert"})
                else:
                    return Response({'msg': "User Not Subscribe Yet"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def sendSubscription(request  ):
    if request.method == 'POST':

                user = Subscribers.objects.filter(email=request.data['email'])
                if user.exists() == False:
                # print("Email Dictionary " , dictionary)
                # key = {{'title': ' Exterior Surface Cleaning Services ', 'State': 'North Carolina', 'category': 'Cleaning, Janitorial and Custodial Services and Supplies', 'link': 'https://www.rfpmart.com/84293-usa-charlotte-north-carolina-exterior-surface-cleaning-services-rfp.html'}, {'title': ' Security Camera System, Access Control Door System and Key Card Printer Maintenance Services ', 'State': 'California', 'category': 'CCTV and Security Services and Supplies', 'link': 'https://www.rfpmart.com/84292-usa-sacramento-california-security-camera-system-access-control-door-system-and-key-card-printer-maintenance-services-rfp.html'}, {'title': ' Strategic Planning Services ', 'State': 'California', 'category': 'Cleaning, Janitorial and Custodial Services and Supplies', 'link': 'https://www.rfpmart.com/84291-usa-california-strategic-planning-services-rfp.html'}}
                    em = request.data['email']
                    sp = re.split(r'[0-1|.|_|-]', em)
                    key={
                        'email':request.data['email']

                    }
                    Subscribers.objects.get_or_create(email=request.data['email'])
                    message = get_template('subscription.html').render(key)
                    email = EmailMessage('Subscription for RFPGurus ', message, to=[em])
                    email.content_subtype = 'html'
                    email.send()
                    return Response({'msg': "Subscribed successfully"})

                    #
                    # key = {
                    #     'dic': sp[0].upper(),
                    #     'email': em
                    # }
                    # print("key",key)



                    # email_list = ['ali.raza@brainplow.com', 'jonybutt3@gmail.com']
                    # email_list = []
                    # email_list.append(request.data['email'])




                else:
                    return Response({'msg':"User Already Exists"} , status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     return Response({'msg': "User Already Exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def unsubscribe(request,email):
    if request.method == 'DELETE':
        if Subscribers.objects.filter(email=email).exists():
            user = Subscribers.objects.get(email=email)
            user.delete()
            message = get_template('unsub_Email.html').render()
            email = EmailMessage('UnSubscribed from RFPGurus', message, to=[user.email])
            email.content_subtype = 'html'
            email.send()
            print('DELETE')
            return Response({'message': "Successfully Unsubscribe"},status=status.HTTP_200_OK)

        else:
         return Response({"message": "Already unsubscribed"},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unsubscribeQuery(request):
    if request.method == 'POST':
        try:
            email = request.data['email']
            comment = request.data['comment']
            obj = UnsubscriberQuery(email=email , comments=comment)
            obj.save()
            return Response({"msg": "Thanks for Response"})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def change_password(request):
    if request.method == 'PUT':
        try:
            pass1 = request.data['pass1']
            pass2 = request.data['pass2']
            print(pass1)
            print(pass2)
            code = request.data['code']
            if Register.objects.filter(authenticate_code=code).exists():
                if (pass1 == pass2):
                    reg_obj = Register.objects.get(authenticate_code=code)
                    usr_obj = User.objects.get(id=reg_obj.user_id)
                    usr_obj.set_password(pass1)
                    usr_obj.save()
                    return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': "Password Not Matched"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'Link Error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'msg': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def postcr(request):

    if request.data['pricepackage'] == 'F':
        try:
            username = request.data['username']
            user = User.objects.get(username=username)
            reg = Register.objects.get(user = user)
            # reg.save()python
            pkg = Packages.objects.get(pkg_type=request.data['pricepackage'])
            payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=False, secret_key=uuid.uuid4())
            payment.end_date = timezone.now().date() + timezone.timedelta(days=30)
            payment.save()
            print("saved")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e,status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        pkg = Packages.objects.get(pkg_type=request.data['pricepackage'], duration=request.data['duration'])
        # print ('price of pkg -----  ',pkg.pkg_price)
        # print(request.data['creditno'])
        # print(request.data['exp'])
        # print(request.data['ccv'])



        dic=request.data


        if "id" in dic and "id" is not None:
            print('in dic')
            detail = PaymentCardInfo.objects.get(id=request.data["id"], user=request.user)
            print("detail", detail)
            exp = detail.expDate
            print("exp", exp)
            credit = detail.number[2:-5]
            cred = detail.number[-4:]

            info = detail.info[2:-1]
            cipher_suite = Fernet(bytes(info,'utf8'))
            plain_text = cipher_suite.decrypt(bytes(credit,'utf8'))
            plain_text1 = str(plain_text)
            number = plain_text1[2:-1] + cred

            creditno = number
            print("credit card ", creditno)
            c=detail.cvc[2:-1]

            cc = cipher_suite.decrypt(bytes(c,'utf8'))
            code = str(cc)[2:-1]
            print("ccv", code)



        else:
            print("not in dic")
            creditno = request.data['creditno']
            exp = request.data['exp']
            code = request.data['ccv']
        authorize.Configuration.configure(
            authorize.Environment.TEST,
            '48Ssg8SJ3Mv',
            '736J4Xm4Vw8bZ392',
            # '8J5w3vWa',
            # '42UME7r5ERN3b5vY',
        )
        result = authorize.Transaction.sale({
            'amount': float(pkg.pkg_price),
            'credit_card': {
                'card_number': creditno,
                'expiration_date': exp,
                'card_code': code,
            }
        })
        print("paid", result)
        #        print(''+request.data['exp'])
        # result = authorize.Transaction.details(result.transaction_response.trans_id)

        if (result['messages'][0]['result_code'] == "Ok"):
            print('hello')
            username = request.data['username']
            user = User.objects.get(username=username)
            reg = Register.objects.get(user=user)
            reg.is_subscribed = True
            reg.save()
            # notify_user()
            # reg.save()
            print ('package--------', pkg)
            print ('package duration--------', pkg.duration)
            if Payment.objects.filter(reg_fk=reg).exists():
                pay = Payment.objects.get(reg_fk=reg)
                log = PaymentLogs(log_reg_fk=pay.reg_fk, log_pkg_fk=pay.pkg_fk, log_is_paid=True,
                                  log_secret_key=pay.secret_key, log_pay_date=pay.pay_date, log_end_date=pay.end_date)
                print(pay)
                log.save()
                pay.delete()

            if pkg.duration == 'M':
                payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                payment.end_date = timezone.now() + timezone.timedelta(days=30)
                payment.save()
                print('j1--------------------------------------------------------')
                print(payment.id)

            elif pkg.duration == 'Q':
                print('j2-------------------------------------')
                payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                payment.end_date = timezone.now() + timezone.timedelta(days=90)
                payment.save()
                # q = []
                # q.append(payment.id)
                # notify_user1(q)
            elif pkg.duration == 'S':
                print('j3-------------------------------------')
                payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                payment.end_date = timezone.now() + timezone.timedelta(days=180)
                payment.save()
                # s = []
                # s.append(payment.id)
                # notify_user2(s)
            else:
                print('j4-------------------------------------')
                payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                payment.end_date = timezone.now() + timezone.timedelta(days=365)
                payment.save()

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_406_NOT_ACCEPTABLE)




@api_view(['POST'])
def pkgsubscribe(request):
    if request.method == 'POST':
        username = request.data['username']
        user = User.objects.get(username=username)
        reg = Register.objects.get(user=user)
        if reg.is_subscribed == True :
            # print("ok")
            return Response({'Response':'Subscribe user'}, status=status.HTTP_200_OK)
        else:
            # print("not ok")
            return Response({'Response':'Not subscribe user'}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['PUT','GET'])
# @permission_classes((IsAuthenticated,))
def Users_details_update(request,username):
    # current_user = request.user
    # print(request.method)
    try:
        user = User.objects.get(username= username)
        profile = Register.objects.get(user=user)
    except Register.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        # serializer1 = Register1Serializer(profile , data=request.data)
        # serializer = Register1Serializer(profile , data=request.data)
        # if serializer.is_valid():
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.username = request.data['username']
            user.save()
            profile.company = request.data['company']
            profile.address = request.data['address']
            profile.zipcode = request.data['zipcode']
            profile.city = request.data['city']
            profile.country = request.data['country']
            profile.state = request.data['state']
            profile.phone_no = request.data['phone']


            profile.save()
            return Response(request.data)
    elif request.method == 'GET':
        serializer = Register2Serializer(profile)
        return Response(serializer.data)



@api_view(['PUT','GET'])
# @permission_classes((IsAuthenticated,))
def preferance_update(request,username):
    # current_user = request.user
    # print(request.method)
    try:
        user = User.objects.get(username= username)
        profile = Register.objects.get(user=user)
    except Register.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        # serializer1 = Register1Serializer(profile , data=request.data)
        # serializer = Register1Serializer(profile , data=request.data)
        # if serializer.is_valid():
        profile.newsletter = request.data['newsletter']
        if 'usercat' in request.data:
            profile.user_preference = request.data['usercat']
        if 'prefersate' in request.data:
            profile.state_preference = request.data['prefersate']
        if 'preferagency' in request.data:
            profile.agency_preference = request.data['preferagency']
        if 'prefercities' in request.data:
            profile.city_preference = request.data['prefercities']
        if 'prefercounty' in request.data:
            profile.county_preference = request.data['prefercounty']

        profile.save()
        return Response(request.data)

    elif request.method == 'GET':
        serializer = Register3Serializer(profile)
        return Response(serializer.data)

@api_view(['POST'])
def email_exist(request):
    # em = "ali.raza@brainplow.com"
    em = request.data['email']
    user = User.objects.filter(email= em).exists()
    print(user)
    if request.method == 'POST' and user == True:
        print("GET Method" )
        serializer = EmailExistSerializer(user)
        # return Response({'Response': 'Email Exist Already'}, status=status.HTTP_200_OK)
        return Response(True)

    else:
        return Response(False)

@api_view(['POST'])
def username_exist(request):
    # em = "ali.raza@brainplow.com"
    uname = request.data['username']
    user = User.objects.filter(username = uname).exists()
    print(user)
    if request.method == 'POST' and user == True:
        print("GET Method" )
        serializer = UserNameCheckSerializer(user)
        # return Response("User Name Already Exists" , True)
        return Response(True)
    else:
        return Response(False)
        # return Response("User Name Not exists", False)


@api_view(['POST'])
def userProfile(request):
    try:
        if (request.method == 'POST'):
            email = request.data['email']
            user_obj = User.objects.get(email=email)
            reg_obj = Register.objects.get(user_id=user_obj.id)
            pay_obj = Payment.objects.get(user_fk_id=reg_obj.id, is_expired=False)
            pkg_obj = Packages.objects.get(pk=pay_obj.pkg_fk_id)
            list1 = []
            # list1.append()
            return Response({
                'name': user_obj.first_name + ' ' + user_obj.last_name,
                'api_key': pay_obj.secret_key,
                'total_called': pay_obj.api_calls,
                'pkg': pkg_obj.pkg_type,
                'pkg_dur': pkg_obj.duration,
                'total_calls': pkg_obj.api_calls,
                'pay_date': pay_obj.pay_date,
                'end_date': pay_obj.end_date,
                'status': pay_obj.is_expired,
                'file_size': pkg_obj.file_size,
                'batch_size': pkg_obj.batch_size,

            }, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
def user_information(request , usernam):
    user = User.objects.filter(username=usernam).exists()
    if user == True:
        print("User found")
        try:
            user = User.objects.get(username=usernam)
            print("User Name" , user.username)
            profile = Register.objects.get(user=user)
            # print(profile)
        except Register.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = Register1Serializer(profile)
            return Response(serializer.data)
        # if request.method == 'PUT':
        #     # history = Register.objects.filter(user=user).update(user_preference=request.data['usercat'])
        #     profile.user_preference = request.data['usercat']
        #     profile.save()
        #     return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def loginchangePassword(request, username):
    if request.method == 'PUT':
        user = User.objects.get(username=username)
        success = (user.check_password(request.data['currentPassword']))
        print("Success", success)
        if success == True:
            if request.data['newPassword'] == request.data['newPassword2']:
                # obj.password = request.data['newPassword']
                user.set_password(request.data['newPassword'])
                print("User", user.password)
                user.save()
                return Response("Your Password has been Successfully changed", status=status.HTTP_200_OK)
            else:
                return Response("Password Not Match",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Incorrect Password", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def customer_social_register_login(request):
    # serializer_class =
    # try:

    temp = request.data["user"]

    socialAuthToken = temp[u"authToken"]
    headers = {
        'Authorization': 'Bearer {0}'.format(socialAuthToken),
        "Content-Type": "application/json"}

    def Facebook():
        social_verification = requests.post("https://graph.facebook.com/v2.8/me", headers=headers)
        return social_verification.status_code == 200

    def Google(token):
        social_verification = requests.get("https://www.googleapis.com/oauth2/v2/tokeninfo?access_token={0}".format(token))

        return social_verification.status_code == 200


    is_valid = Facebook() if temp[u"provider"] == "FACEBOOK" else Google(socialAuthToken)

    if is_valid:



        """if (email_verifying(request.data['email'])):
            return generate_email_error()

        if (username_verifying(request.data['username'])):
            return generate_username_error()
        """
        password = "{0}{1}{2}".format(temp["provider"], temp["id"], "rfpgurus")

        try:
            # return token if user exists
            object_user = Register.objects.get(social_id=temp["id"],social_provider=temp["provider"]).user
            payload = jwt_payload_handler(object_user)
            token = jwt_encode_handler(payload)

        except Exception as e:
            # create user and return token
            username = "{0}_{1}_{2}".format(temp["provider"], temp["id"], temp["name"]).lower()
            username = re.sub("[^\+\d\w_@\.-]+","",username)

            object_user = User(username=username)
            # if (temp["firstName"] is not None):
            #     object_user.first_name = temp["firstName"]
            # if(temp["lastName"] is not None):
            #     object_user.last_name = temp["lastName"]
            if(temp["email"] is not None):
                object_user.email = temp["email"]

            object_user.set_password(password)
            object_user.save()
            profile = Register(
                is_authenticated=True,
                newsletter=True,
                is_social=True,
                user=object_user,
                social_id = temp["id"],
                social_provider = temp["provider"],
                # profilePhoto = temp["photoUrl"]
                # user=object_user
            )

            profile.save()

            payload = jwt_payload_handler(object_user)
            token = jwt_encode_handler(payload)

        return HttpResponse(json.dumps({"token": token}))


# Practice data
#
# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
# @api_view(['GET'])
# def prac(request):
#     session = Session.objects.all()
#     print(session)
#     for i in session:
#         uid = i.get_decoded().get('_auth_user_id')
#         #session_data = i.get_decoded()
#         #print uid
#
#         return Response()
#
# @api_view(['GET'])
# def preventuserloginagain(request):
#     session_list=[]
#     id_list=[]
#     j=0
#     try:
#         q = User.objects.get(id=363)
#     except:
#         return Response('Username does not exist',status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#
#         print('user here is >>>',q.id)
#         session = Session.objects.all()
#         #print('sesssionnnn..',session)
#         for i in session:
#             #print(i)
#             uid = i.get_decoded().get('_auth_user_id')
#             session_list.append(uid)
#
#             if(str(uid)==str(q.id)):
#
#                 id_list.append(i)
#
#         #for j in session_list
#         print('SESSIONLIST>>>>>>', session_list)
#         print('specific_session>>>>>>', id_list)
#         #print(session_list[0])
#
#         for j in range(len(id_list)):
#             session = Session.objects.get(session_key=id_list[j])
#             print("specific",session)
#             #session.delete()
#
#         #print('Id_LIST>>>>>>', id_list)
#         if str(q.id) in session_list:
#             return Response('Connection Already Establish...!!!')
#         else:
#             return Response('No Connection...!!!')
#



@api_view(['GET'])
def allagenncies(request):
    if request.method =='GET':
        list=Allagencies.objects.all()
        serializers=AllagenciesSerializer(list,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def cites(request):
    if request.method == 'GET':
        list = City.objects.all()
        serializers = CitesSerializer(list, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def county(request):
    if request.method == 'GET':
        list = County.objects.all()
        serializers = CountySerializer(list, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


