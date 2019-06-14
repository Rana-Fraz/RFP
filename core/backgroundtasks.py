from background_task import background
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from user_payment.models import Payment
from core.models import Register,Packages

@background(schedule=2592000)
def notify_user(id):
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    print('Back ...................... ground')
    print(id[0])
    obj = Payment.objects.get(id=id[0])
    print(obj)
    obj.is_paid = False
    obj.is_expired = True
    obj.save()
    print('jjjjjjjjj3333')
    print('Updated')

    print(obj)
    reg = Register.objects.get(user=User.objects.get(username=obj))
    print('Register.......')
    print(reg )
    reg.is_subscribed = False
    reg.save()
    return Response({'Response':'Ok Background'}, status=status.HTTP_200_OK)

@background(schedule=7776000)
def notify_user1(id):
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    print('Back ...................... ground')
    print(id[0])
    obj = Payment.objects.get(id=id[0])
    print(obj)
    obj.is_paid = False
    obj.is_expired = True
    obj.save()
    print('Updated')

    print(obj)
    reg = Register.objects.get(user=User.objects.get(username=obj))
    print('Register.......')
    print(reg)
    reg.is_subscribed = False
    reg.save()
    return Response({'Response':'Ok Background'}, status=status.HTTP_200_OK)

@background(schedule=15552000)
def notify_user2(id):
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    print('Back ...................... ground')
    print(id[0])
    obj = Payment.objects.get(id=id[0])
    print(obj)
    obj.is_paid = False
    obj.is_expired = True
    obj.save()
    print('Updated')

    print(obj)
    reg = Register.objects.get(user=User.objects.get(username=obj))
    print('Register.......')
    print(reg)
    reg.is_subscribed = False
    reg.save()
    return Response({'Response':'Ok Background'}, status=status.HTTP_200_OK)

@background(schedule=31104000)
def notify_user3(id):
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    print('Back ...................... ground')
    print(id[0])
    obj = Payment.objects.get(id=id[0])
    print(obj)
    obj.is_paid = False
    obj.is_expired = True
    obj.save()
    print('Updated')

    print(obj)
    reg = Register.objects.get(user=User.objects.get(username=obj))
    print('Register.......')
    print(reg)
    reg.is_subscribed = False
    reg.save()
    return Response({'Response':'Ok Background'}, status=status.HTTP_200_OK)
