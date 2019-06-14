from django.db.models import Q
from django.shortcuts import render
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Bloginfo,BecomePartner
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rfp.models import *
import datetime
from core.models import Register
# Create your views here.
@api_view(['GET'])
def bloglist(request):
     if Bloginfo.objects.exists():
         blog = Bloginfo.objects.all().order_by('-publish_date')
         serializers = BlogSerializers(blog , many=True)
         return  Response(serializers.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def singleblog(request,bid):
    if Bloginfo.objects.filter(id=bid).exists():
        singledata = Bloginfo.objects.filter(id=bid)
        serializers = BlogSerializers(singledata,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)



@api_view(['POST'])
def becomePartner(request):
    if request.method == 'POST':
        serializer=BecomePartnerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def first_notifications(request):
    if request.method == 'GET':
        try:
            print("user",request.user.id)
            user_reciver = User.objects.get(id=request.user.id)
        except:
            return Response({'Message':'User does not exist'})

        sendNotification(request.user.id)
        list= Notification_Detail.objects.filter(receiver=user_reciver.id).exclude(isdeleted=True)
        unread=Notification_Detail.objects.filter(receiver=user_reciver.id,read=False).exclude(isdeleted=True).exclude(read=True)

        serializer=NotifySerializer(list,many=True)
        data={
            "unread":unread.count(),
            "notifications":serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def read_delete(request,id):
    try:
        record=Notification_Detail.objects.get(id=id)
    except:
        return Response("Notification does not exists",status=status.HTTP_404_NOT_FOUND)

    if request.method=='PUT':
        record.read=True
        record.save()
        return Response({"Message":"Read Notification done"},status=status.HTTP_200_OK)

    if request.method=='DELETE':
        record.isdeleted=True
        record.save()
        return Response({"Message": "Deleted notification"}, status=status.HTTP_200_OK)
    return Response("Neither Deleted nor Read",status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_all_notification(request):
    try:
        user=User.objects.get(pk=request.user.id)
    except:
        return Response("User does not exists",status=status.HTTP_404_NOT_FOUND)

    if request.method=='DELETE':
        data=Notification_Detail.objects.filter(receiver=user)
        for i in data:
            i.isdeleted=True
            i.save()
        print(data)
        return Response({"Message": "Deleted notifications"}, status=status.HTTP_200_OK)
    return Response("Something went wrong",status=status.HTTP_400_BAD_REQUEST)



def sendNotification(user_reciver):
    #
    # now = datetime.datetime.now()
    # split = str(now)[:-15]
    #
    # results = DataCleaning_GovernmentBidsProfile.objects.filter(date_entered__gte=split).order_by('date_entered')[0:4]

    user_reciver = User.objects.get(id=user_reciver)
    #test = User.objects.filter(is_staff=True)[:1]
    # sender=User.objects.get(id=test[0].id)
    # print(sender.id)

    now = datetime.datetime.now()
    split = str(now)
    print(split)
    new = split[0:10]
    print ('new', new)
    list = []
    reg = Register.objects.filter(user=user_reciver)
    for a in reg:
        prefer_state = a.state_preference
        prefer_city = a.city_preference
        prefer_county = a.county_preference
        prefer_agency = a.agency_preference
        prefer_category = a.user_preference
        que = Q()
        if a.state_preference is not None:
            for i in prefer_state:
                que |= Q(state__icontains=i)
               # print("state", que)
        if a.city_preference is not None:
            for i in prefer_city:
                que |= Q(city__icontains=i)
                #print("city", que)

        if a.county_preference is not None:
            for i in prefer_county:
                que |= Q(city_or_county__icontains=i)
                #print("county", que)

        if a.agency_preference is not None:
            for i in prefer_agency:
                que |= Q(agency__icontains=i)
               # print("agency", que)

        if a.user_preference is not None:
            for i in prefer_category:
                que |= Q(category__icontains=i)
                #print("category", que)

        results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte=new).filter(date_entered=new).filter(
            que).exclude(title="").exclude(agency="").exclude(seoTitleUrl="")
        #serializers = GovernmentBids_emailSerializers(results, many=True)


    for i in results:
        des='Check Out New RFP " '+i.title+'"'
        link=i.seoTitleUrl
        title=i.agency

        if Notification_Detail.objects.filter(description=des,receiver=user_reciver).exists():
            print("Already exist")

            pass

        else:
            Notification_Detail.objects.get_or_create(receiver=user_reciver,type_of_notification=title,description=des,target=link)










