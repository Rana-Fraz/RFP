# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from jwt_auth.compat import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from rfp.scheduler_for_email import package_unsubmail
from triggerr.models import notification_test_data
from .serializers import PurchaseHistorySerializer,CardSerializer,CardPostSerializer,updateCardSerializer
from django.shortcuts import render
from .models import Payment,PaymentLogs,PaymentCardInfo
from core.models import Register,Packages
import datetime
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import authorize
import uuid
from cryptography.fernet import Fernet
from copy import deepcopy

from django.core.mail import send_mail
# Create your views here.


@api_view(['GET','POST','PUT'])
@permission_classes((IsAuthenticated,))
def Purchase(request, username):
    # try:
        #user = User.objects.get(username=username)
        reg = Register.objects.get(user=request.user)
        print(reg)
        # if request.method == 'GET':
        #     try:
        #         if Payment.objects.filter(reg_fk=reg).exists():
        #             history = Payment.objects.filter(reg_fk=reg)
        #         else:
        #             return Response({"Error": "You don't have any subscribe package"}, status=404)
        #         serializer = PurchaseHistorySerializer(history,many=True)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     except :
        #         return Response({"Error": "You don't have any subscribe package"},status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # print(request.data['pkgdate'])
            # now = datetime.datetime.now()
            # split = str(now)[:-15]

            print("Getttttt ")
            #
            # user = User.objects.get(username=username)
            # reg = Register.objects.get(user=user)

            if Payment.objects.filter(reg_fk=reg).exists():
                payment_obj = Payment.objects.get(reg_fk=reg)
                package_unsubmail()
                # print(payment_obj)
                # print("payment_obj.reg_fk.user.email",payment_obj.reg_fk.user.email)
                # now = timezone.now()
                # if now.date() >= payment_obj.end_date:
                #     payment_obj.is_expired = True
                #     payment_obj.is_paid = False
                #     reg.is_subscribed = False
                #     payment_obj.save()
                #     reg.save()
                #     send_mail(
                #         subject="RFPGurus Package Deactivated",
                #         message="Your Package has been deactivated",
                #         from_email="no-reply@rfpgurus.com",
                #         recipient_list=[payment_obj.reg_fk.user.email],
                #         fail_silently=False)
                #     print("mail sent")
                #     serializer = PurchaseHistorySerializer(payment_obj)
                #     return Response(serializer.data, status=status.HTTP_200_OK)
                # else:
                serializer = PurchaseHistorySerializer(payment_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "You don't have any subscribe package"}, status=404)

            # if request.data['pkgdate'] <= split :
            #     history = Payment.objects.filter(reg_fk=reg).update(is_paid = False,is_expired= True)
            #     user = Register.objects.filter(user = user).update(is_subscribed= False)
            #     # history.save()
            #     # user.save()
            #     return Response(True,status=status.HTTP_200_OK)
        if request.method == 'PUT':
            print("jony")
            pkg = Packages.objects.get(pkg_type=request.data['pricepackage'], duration=request.data['duration'])
            print('price of pkg -----  ', pkg.pkg_price)
            print(request.data['creditno'])
            print(request.data['exp'])
            print(request.data['ccv'])
            authorize.Configuration.configure(
                authorize.Environment.TEST,
                '48Ssg8SJ3Mv',
                '736J4Xm4Vw8bZ392',
            )
            result = authorize.Transaction.sale({
                'amount': float(pkg.pkg_price),
                'credit_card': {
                    'card_number': request.data['creditno'],
                    'expiration_date': request.data['exp'],
                    'card_code': request.data['ccv'],
                }
            })
            print(result)
            print('' + request.data['exp'])
            # result = authorize.Transaction.details(result.transaction_response.trans_id)

            if (result['messages'][0]['result_code'] == "Ok"):
                # username = request.data['username']
                # user = User.objects.get(username=username)
                # reg = Register.objects.get(user=user)
                reg.is_subscribed = True
                reg.save()
                print('package--------', pkg)
                print('package duration--------', pkg.duration)

                if Payment.objects.filter(reg_fk=reg).exists():
                    pay = Payment.objects.get(reg_fk=reg)
                    log = PaymentLogs(log_reg_fk=pay.reg_fk, log_pkg_fk=pay.pkg_fk, log_is_paid=True, log_secret_key=pay.secret_key, log_pay_date = pay.pay_date , log_end_date= pay.end_date)
                    print(pay)
                    log.save()
                    pay.delete()

                if pkg.duration == 'M':
                    print('j1-------------------------------------')


                    payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                    payment.end_date = timezone.now() + timezone.timedelta(days=30)
                    payment.save()
                    print(payment.reg_fk,'j1--------------------------------------------------------')
                    print(payment.id)

                elif pkg.duration == 'Q':
                    print('j2-------------------------------------')
                    # pay = Payment.objects.get(reg_fk=reg)
                    # pay.delete()
                    payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                    payment.end_date = timezone.now() + timezone.timedelta(days=90)
                    payment.save()
                elif pkg.duration == 'S':
                    print('j3-------------------------------------')
                    # pay = Payment.objects.get(reg_fk=reg)
                    # pay.delete()
                    payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                    payment.end_date = timezone.now() + timezone.timedelta(days=180)
                    payment.save()
                else:
                    print('j4-------------------------------------')
                    # pay = Payment.objects.get(reg_fk=reg)
                    # pay.delete()
                    payment = Payment(reg_fk=reg, pkg_fk=pkg, is_paid=True, secret_key=uuid.uuid4())
                    payment.end_date = timezone.now() + timezone.timedelta(days=365)
                    payment.save()

                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_406_NOT_ACCEPTABLE)
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

#
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def cardno(request):
#     if request.method == 'POST':
#         dic = request.data
#         dic.update({"user": request.user.id})
#         credit = request.data['number']
#         count1 = PaymentCardInfo.objects.filter(user=reques t.user.id)
#         for i in count1:
#             if (i.number == credit):
#                 return Response({'message': 'Crad Number already exist'}, status=status.HTTP_302_FOUND)
#         return Response(status=status.HTTP_200_OK)




@api_view(['GET','POST','PUT'])
@permission_classes((IsAuthenticated,))
def cardInfo(request):
    if request.method == 'GET':
        try:
            info = PaymentCardInfo.objects.filter(user=request.user.id)
            if not info:
                return Response({'state':False,'message': 'No Credit card detail in your list'},
                                status= status.HTTP_202_ACCEPTED)
        except PaymentCardInfo.DoesNotExist:
            return Response({'state':False,'message': 'No Credit card detail in your list'},
                                status= status.HTTP_202_ACCEPTED)

        d = request.user.id
        lt = []

        for i in info:
            if i.card_type == 'American Express':
                cred = i.number[-4:]

                cardnumber = '***********' + cred
                ccv = '****'


            else:
                cred = i.number[-4:]

                cardnumber = '************' + cred
                ccv = '***'


            res = {
                'id': i.id,
                'ccv': ccv,
                'card_type': i.card_type,
                'expiryDate': i.expDate,
                'cardNumber': cardnumber,
                'zipcode':i.zipcode,
                'default': i.default,
                'nickname': i.name,
                'street_address':i.street_address,
                'city':i.city,
                'state':i.state,
                'country':i.country,
                'autopay':i.autopay

            }
            lt.append(res)
        return  Response(lt, status = status.HTTP_200_OK)

    if request.method == 'POST':
            dic = request.data
            print("dic",dic)
            exist=False
            dic.update({"user": request.user.id})
            print("updated dic",dic)

            creditno1=request.data['number']
            ccv=request.data['cvc']

            auto=request.data['autopay']

            key = Fernet.generate_key()
            print("key",key)
            dic.update({'info':str(key)})
            cipher_suite = Fernet(key)

            if dic['card_type'] == 'American Express':
                creditno2 = creditno1[0:11]
                code2 = creditno1[11:]
                encreditno = cipher_suite.encrypt(bytes(creditno2,'utf8'))
                print("encode",encreditno)
                creditno = str(encreditno) + code2
                print("creditcard to store", creditno)

                dic.update({'number': creditno})

            else:
                creditno3 = creditno1[0:12]
                code3 = creditno1[12:]

                encreditno = cipher_suite.encrypt(bytes(creditno3,'utf8'))
                creditno = str(encreditno) + code3
                print("creditcard to store", creditno)

                dic.update({'number': creditno})

            ccv = cipher_suite.encrypt(bytes(ccv,'utf8'))
            dic.update({'cvc': str(ccv)})

            print("dic", dic)
            check = request.data['default']

            # Actual code
            count1 = PaymentCardInfo.objects.filter(user=request.user.id)
            count = count1.count()
            print("count", count)

            if (count == 0):
                print("every first time")
                serializer = CardPostSerializer(data=dic)
                if serializer.is_valid():
                    serializer.save()
                    obj = serializer.save()
                    if obj.id:
                        info = PaymentCardInfo.objects.filter(user=request.user)
                        serializers1 = CardSerializer(info, many=True)
                        return Response(serializers1.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                if (count >= 5):
                    return Response({'message': 'You cannot enter card more than 5'}, status=status.HTTP_403_FORBIDDEN)

                elif (count > 0 and count <= 5):
                    for i in count1:
                        print("full data",i.number)
                        c1 =i.number[2:-5]
                        print("for decryt",c1)

                        cred = i.number[-4:]
                        print("card 4",cred)
                        #print("last 4",cred)

                        info1 = i.info[2:-1]

                        # utf16string = info1.encode("utf-16")
                        # #info= base64.b64encode(bytes(info1,'utf8'))
                        # #info= base64.urlsafe_b64decode(info1)
                        # info=(bytes(info1,'utf8'))
                        # string = info.decode("utf-8").encode("utf-16")
                        # info
                        # info=base64.urlsafe_b64decode(info1)
                        # print("type",type(info))


                        cipher_suite = Fernet(bytes(info1,'utf8'))

                        plain_text = cipher_suite.decrypt(bytes(c1,'utf8'))
                        print("after decryption",plain_text)
                        plain_text1=str(plain_text)
                        number = plain_text1[2:-1] + cred
                        print("end result",number)


                        if (str(number) == str(creditno1)):
                            exist = True
                            return Response({'message': 'Crad Number already exist'}, status=status.HTTP_302_FOUND)

                        else:
                            exist = False

                    if (exist == False):
                        if(auto == True):
                            card = PaymentCardInfo.objects.filter(user=request.user.id)
                            for i in card:
                                if (i.autopay == True):
                                    print(i.default)
                                    i.autopay = False
                                    i.save()

                        if (check == True):
                            print(check)
                            card = PaymentCardInfo.objects.filter(user=request.user.id)
                            for i in card:
                                if (i.default == True):
                                    print(i.default)
                                    i.default = False
                                    i.save()
                        print ("dic",dic)
                        serializer = CardPostSerializer(data=dic)
                        if serializer.is_valid():
                            serializer.save()

                            obj = serializer.save()
                            if obj.id:
                                info = PaymentCardInfo.objects.filter(user=request.user)
                                serializers = CardSerializer(info, many=True)
                                return Response(serializers.data, status=status.HTTP_201_CREATED)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:

                        return Response({'message': 'Crad Number already exist'}, status=status.HTTP_302_FOUND)
                else:
                    return Response({'message': 'You cannot enter card more than 5'}, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'PUT':
        dic = request.data
        cid = dic['cid']
        check = request.data['default']

        count1 = PaymentCardInfo.objects.filter(user=request.user.id)

        auto = request.data['autopay']

        if (auto == True):
            card = PaymentCardInfo.objects.filter(user=request.user.id)
            for i in card:
                if (i.autopay == True):
                    print(i.default)
                    i.autopay = False
                    i.save()



        if (check == True):
                    print(check)
                    card = PaymentCardInfo.objects.filter(user=request.user.id)
                    for i in card:
                        if (i.default == True):
                            print(i.default)
                            i.default = False
                            i.save()

        info = PaymentCardInfo.objects.get(user=request.user,id=cid)
        serializer = updateCardSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def cardInfoDelete(request,id):
    if request.method == 'DELETE':
        if PaymentCardInfo.objects.filter(user=request.user, id=id).exists():
            checkout = PaymentCardInfo.objects.filter(user=request.user, id=id)
            if not checkout:
                return Response({'status': False,
                                 'message': 'Not Found requested Item in your Card List'},
                                status=status.HTTP_202_ACCEPTED)
            checkout.delete()
            return Response({'message': 'Deleted Finally', 'status': True}, status=status.HTTP_202_ACCEPTED)
        return Response({'status': False,
                         'message': 'Not Found requested Item in your Card List'},
                        status=status.HTTP_202_ACCEPTED)

from user_payment.autopay import autopay
@api_view(['GET'])
def cardno(request):
    if request.method == 'GET':

        autopay()
        return Response(status=status.HTTP_200_OK)