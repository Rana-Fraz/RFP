# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# from jwt_auth.compat import User
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import permissions
# from rest_framework.response import Response
# from rest_framework import status
# # from .serializers import PurchaseHistorySerializer
# from django.shortcuts import render
# # from .models import Payment
# from core.models import Register
# import datetime
# from rest_framework.permissions import IsAuthenticated
#
# # Create your views here.
#
#
# @api_view(['GET','POST'])
# @permission_classes((IsAuthenticated,))
# def Purchase(request, username):
#  try:
#     user = User.objects.get(username=username)
#
#     reg = Register.objects.get(user=user)
#
#
#     if request.method == 'GET':
#
#      try:
#       print(request.user.id)
#       history = Payment.objects.filter(reg_fk=reg)
#       print(history)
#       serializer = PurchaseHistorySerializer(history,many=True)
#       return Response(serializer.data, status=status.HTTP_200_OK)
#
#      except:
#          return Response(status=status.HTTP_404_NOT_FOUND)
#
#     elif request.method == 'POST':
#         print(request.data['pkgdate'])
#         now = datetime.datetime.now()
#         split = str(now)[:-15]
#         print(split)
#         if request.data['pkgdate'] <= split :
#             history = Payment.objects.filter(reg_fk=reg).update(is_paid = False,is_expired= True)
#             user = Register.objects.filter(user = user).update(is_subscribed= False)
#             history.save()
#             user.save()
#
#         return Response(True,status=status.HTTP_200_OK)
#
#  except:
#      Response(status=status.HTTP_400_BAD_REQUEST)