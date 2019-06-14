from __future__ import unicode_literals

from dateutil import parser

from django.db import connection
import os
from datetime import timedelta
import pandas as pd
import paramiko as paramiko
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import get_template
from rest_framework.decorators import api_view, permission_classes
import math
from django.db.models import F

# Create your views here.
# -*- coding: utf-8 -*-

# Create your views here.
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status, permissions

from core.models import Register
# from scrappers.goodSite import da
from .models import *

from django.utils import timezone
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from jwt_auth.compat import User

#
# import base64
# import string
# import random
# from django.contrib.auth.models import User;
# from django.template.loader import get_template
# from django.core.mail import EmailMessage
# import uuid
# from itertools import chain
# from django.views.decorators.csrf import csrf_exempt
# from itertools import chain
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import TemplateHTMLRenderer
# from  rest_framework.views import APIView
# from django.db import transaction,IntegrityError
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import permissions
from django.db.models import Count
import datetime


@api_view(['GET'])
def searchCategory(request, query):
    que = Q()
    # que &= Q(date_entered__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$')
    # que &= Q(due_date__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$')

    #que = Q()
    for word in query.split():
        print(word)
        que &= Q(category__icontains=word)
        print(que)
    # que = Q(state__icontains=query)
    print("Que", que)
    if request.method == 'GET':
        results = DataCleaning_GovernmentBidsProfile.objects.filter(que).distinct('category')
        paginator = Paginator(results, 10)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        serializer_context = {'request': request}
        serializer = CategorySerializer(data, many=True, context=serializer_context)
        items = paginator.count
        pages = paginator.num_pages

        res = {
            'totalItems': items,
            'totalPages': pages,
            'results': serializer.data,

        }
        return Response(res)


@api_view(['GET'])
def getCity(request, query):
    if request.method == 'GET':
        try:
            results = DataCleaning_GovernmentBidsProfile.objects.filter(state__contains=query).exclude(state__exact='')
            serializer = CityBidsSerializers(results, many=True)
            res = {

                'Results': serializer.data

            }
            return Response(res)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def searchState(request, query):
    que = Q()

    for word in query.split():
        print(word)
        que &= Q(state__icontains=word)
        print(que)

    print("Que", que)
    if request.method == 'GET':
        try:
            results = DataCleaning_GovernmentBidsProfile.objects.filter(que).exclude(state__exact='').distinct('state')
            # results = DataCleaning_GovernmentBidsProfile.objects.filter(title__contains=query)
            paginator = Paginator(results, 10)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            serializer = StateSerializer(data, many=True, context=serializer_context)
            items = paginator.count
            pages = paginator.num_pages

            res = {
                'totalItems': items,
                'totalPages': pages,
                'results': serializer.data,

            }
            return Response(res)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def searchRfpID(request, query):

    que = Q()
    # que &= Q(date_entered__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$')
    # que &= Q(due_date__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$')
    for word in query.split():
        print(word)
        que &= Q(rfp_number__icontains=word) | Q(deescription__icontains=word)
        print(que)
    # que = Q(state__icontains=query)
    print("Que", que)
    if request.method == 'GET':
        results = DataCleaning_GovernmentBidsProfile.objects.filter(que)
        # results = DataCleaning_GovernmentBidsProfile.objects.filter(title__contains=query)
        paginator = Paginator(results, 10)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        serializer_context = {'request': request}
        serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
        items = paginator.count
        pages = paginator.num_pages

        res = {
            'totalItems': items,
            'totalPages': pages,
            'results': serializer.data,

        }
        return Response(res)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def searchRfp(request, query, items):
    if request.method == 'GET':
        try:
            items = int(items)

            que = Q()
            for word in query.split():
                print(word)
                que &= Q(rfp_number__icontains=word) | Q(title__icontains=word) | Q(state__icontains=word) | Q(
                    category__icontains=word)
                print(que)
                # que = Q(state__icontains=query)
                print("Que", que)
            results = DataCleaning_GovernmentBidsProfile.objects.filter(que)
            # results = DataCleaning_GovernmentBidsProfile.objects.filter(title__contains=query)
            paginator = Paginator(results, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            print(request.user.id)
            if request.user.id:
                print("junaid1")
                if Register.objects.get(user=request.user.id).is_subscribed:
                    print("junaid2")
                    serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)

                else:
                    print("junaid3")
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

            else:
                print("junaid4")

                serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

            items = paginator.count
            pages = paginator.num_pages
            res = {
                'totalItems': items,
                'totalPages': pages,
                'results': serializer.data

            }
            return Response(res)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def searchRfp_total(request,query,items):
    query = "'" + query + "'"
    get_all_items = 'Select Count(*) from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    get_all_data = get_all_items.format(",".join, query)
    print("query")
    print(get_all_data)
    with connection.cursor() as cursor:
        cursor.execute(get_all_data)
        print("cursor")
        fetch_items = cursor.fetchall()
        num_items = [x[0] for x in fetch_items]
        print(num_items[0])

        # print(int(num_items[0]))
        print(items)
        total_pages = (int(num_items[0])/ int(items))
        res = {
            'totalItems': num_items[0],
            'totalPages': math.ceil(total_pages)
        }
        return Response(res,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def searchRfp_raw(request,query, items):
    query="'"+query+"'"
    print("queryyy  ", query)
    print("item  ", items)
    res = {}
    if request.GET.get('page') == 1:
        offset = 0
        print("page 2 ", offset)
    else:
        offset = (int(request.GET.get('page')) * int(items)) - int(items)
        print("page 2 ", offset)
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) or "category" ~*  {1} or "state" ~*  {1} or "rfp_number" ~*  {1}'
    if (str(items) == '-1'):
        print("get all")
        main_data_query = 'Select {0} from rfp_governmentbidsprofile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    else:
        print("not all")
        main_data_query = 'Select {0} from rfp_governmentbidsprofile  where  "tsv_title" @@ plainto_tsquery({1}) limit {2} offset {3}'
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where "title" ~* {1}'

    print('query  ')
    print(main_data_query)


    print(main_data_query)
    if request.user.id:
        if Register.objects.get(user=request.user.id).is_subscribed:
            fields = [
                "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
                "due_date", "web_info", "rfp_reference","seoTitleUrl"
            ]
        else:
            fields = [
                "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
                "due_date","seoTitleUrl"

            ]
    else:
        fields = [
            "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
            "due_date","seoTitleUrl"

        ]
    out = ['"{0}"'.format(i) for i in fields]

    temp=[]
    extra_fields = []
    fields.extend(extra_fields)

    out.extend(['cast("{0}" as varchar)'.format(i) for i in extra_fields])

    if(int(items)!=-1):
        data_query = main_data_query.format(",".join(out), query, items, offset)
    else:
        data_query = main_data_query.format(",".join(out), query)


    # get_all_items = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    # get_all_data = get_all_items.format(",".join(out), query)


    print(data_query)
    f_count = len(fields)

    with connection.cursor() as cursor:
        cursor.execute(data_query)

        for i in cursor.fetchall():

            # if i[5] > 0:
            # print (i)
            current_item = {}
            for j in range(f_count):

                current_item[fields[j]] = i[j]

            temp.append(current_item)


        print("junaid")
        print(len(temp))
        print(len(temp)/int(items))
        # paginator = Paginator(temp, items)
        # page = request.GET.get('page')
        # try:
        #     data = paginator.page(page)
        # except PageNotAnInteger:
        #     data = paginator.page(1)
        # except EmptyPage:
        #     data = paginator.page(paginator.num_pages)

        # res["results"] = temp
        # items = paginator.count
        # pages = paginator.num_pages
        # result = res;
        res = {
            'totalItems': len(temp),
            'totalPages': 0,
            'results': temp

        }
        return Response(res,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def searchRfp_withsorting(request,query, items,search,order):
    query="'"+query+"'"
    print("queryyy  ", query)
    print("item  ", items)
    res = {}
    if request.GET.get('page') == 1:
        offset = 0
        print("page 2 ", offset)
    else:
        offset = (int(request.GET.get('page')) * int(items)) - int(items)
        print("page 2 ", offset)
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) or "category" ~*  {1} or "state" ~*  {1} or "rfp_number" ~*  {1}'
    if (str(items) == '-1'):
        print("get all")
        main_data_query = 'Select {0} from rfp_governmentbidsprofile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    else:
        main_data_query = 'Select {0} from rfp_governmentbidsprofile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
        print("not all")
        #main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) limit {2} offset {3}'
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where "title" ~* {1}'

    print('query  ')
    print(main_data_query)


    print(main_data_query)
    if request.user.id:
        if Register.objects.get(user=request.user.id).is_subscribed:
            fields = [
                "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
                "due_date", "web_info", "rfp_reference","seoTitleUrl"
            ]
        else:
            fields = [
                "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
                "due_date","seoTitleUrl"

            ]
    else:
        fields = [
            "id", 'rfpkey', "rfp_number", "title", "deescription", "category", "state", "agency", "date_entered",
            "due_date","seoTitleUrl"

        ]
    out = ['"{0}"'.format(i) for i in fields]

    temp=[]
    extra_fields = []
    fields.extend(extra_fields)

    out.extend(['cast("{0}" as varchar)'.format(i) for i in extra_fields])

    if(int(items)!=-1):
        data_query = main_data_query.format(",".join(out), query, items, offset)
    else:
        data_query = main_data_query.format(",".join(out), query)


    print(data_query)
    f_count = len(fields)

    with connection.cursor() as cursor:
        cursor.execute(data_query)

        for i in cursor.fetchall():

            # if i[5] > 0:
            # print (i)
            current_item = {}
            for j in range(f_count):

                current_item[fields[j]] = i[j]

            temp.append(current_item)


        newlist=[]
        search1=search
        if(order=='asc'):
         newlist = sorted(temp, key=lambda k: k[search1])

        if (order == 'dec'):
            newlist = sorted(temp, key=lambda k: k[search1], reverse=True)

        # print("junaid")
        # print(len(temp))
        # print(len(temp)/int(items))

        paginator = Paginator(newlist, items)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        serializer_context = {'request': request}
        if request.user.id:
            if Register.objects.get(user=request.user.id).is_subscribed:
                serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)

            else:
                serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

        else:

            serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

        items = paginator.count
        pages = paginator.num_pages
        res = {
            'totalItems': items,
            'totalPages': pages,
            'results': serializer.data

        }
        return Response(res,status=status.HTTP_200_OK)



@api_view(['GET'])
def latestRfp(request, items):

        if request.method == 'GET':
            print("in get")
            items = int(items)
            print("items",items)
            now = datetime.datetime.now()
            print(now)
            split = str(now)[0:11]
            print(split)

            week_ago1 = now - datetime.timedelta(days=7)
            print("week",week_ago1)

            week_ago = str(week_ago1)[0:11]
            print("week_ago", str(week_ago))

            # results=GovernmentBidsProfile.objects.filter(timestamp__range=[week_ago,split]).order_by('-date_entered').exclude(date_entered__isnull=True)
            results = DataCleaning_GovernmentBidsProfile.objects.filter(date_entered__gte=week_ago).order_by(
                '-date_entered').exclude(date_entered__isnull=True)
            paginator = Paginator(results, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            if request.user.id:
                if Register.objects.get(user=request.user.id).is_subscribed:
                    serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)

                else:
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

            else:

                serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

            items = paginator.count
            pages = paginator.num_pages
            res = {
                'totalItems': items,
                'totalPages': pages,
                'results': serializer.data

            }
            return Response(res)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def searchTitle(request, query):

    que = Q()
    for word in query.split():
        print(word)
        que &= Q(title__icontains=word)
        print(que)
    # que = Q(title__icontains=query)
    print("Que", que)
    if request.method == 'GET':
        results = DataCleaning_GovernmentBidsProfile.objects.filter(que)
        # results = DataCleaning_GovernmentBidsProfile.objects.filter(title__contains=query)
        paginator = Paginator(results, 10)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        serializer_context = {'request': request}
        serializer = GovernmentBidsSerializers(data, many=True, context=serializer_context)
        items = paginator.count
        pages = paginator.num_pages

        res = {
            'totalItems': items,
            'totalPages': pages,
            'results': serializer.data,

        }
        return Response(res)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def rfp(request, sort, order, items):
    if request.method == 'GET':
        try:
            items = int(items)
            try:
                if (order == 'asc'):
                    sort_by = '-' + sort
                else:
                    sort_by = sort
            except:
                return Response({'msg': 'wrong query parameters'}, status=status.HTTP_400_BAD_REQUEST)
            if request.user.id:
                user = Register.objects.get(user=request.user.id)

                if user.user_preference is not None:
                    print("junaid0")
                    if sort == 'due_date':
                        juni = DataCleaning_GovernmentBidsProfile.objects.filter(due_date__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$',
                                                                category__in=user.user_preference).order_by(sort_by)
                    elif sort == 'date_entered':
                        juni = DataCleaning_GovernmentBidsProfile.objects.filter(date_entered__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$',
                                                                    category__in=user.user_preference
                                                                    ).exclude(
                        state__exact='').exclude(rfpkey__exact='').exclude(rfpkey__isnull=True).order_by(sort_by)


                    else:
                        juni = DataCleaning_GovernmentBidsProfile.objects.filter(category__in=user.user_preference).exclude(
                        state__exact='').exclude(rfpkey__exact='').order_by(sort_by)
                    print(request.user.id)
                else:
                    print("junaid1")
                    if sort == 'due_date':
                        juni = DataCleaning_GovernmentBidsProfile.objects.filter(
                            due_date__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$').order_by(sort_by)
                    elif sort == 'date_entered':
                        juni = DataCleaning_GovernmentBidsProfile.objects.filter(
                            date_entered__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$').exclude(state__exact='').exclude(
                            rfpkey__exact='').exclude(rfpkey__isnull=True).order_by(sort_by)

                    # elif sort == 'rfpkey':
                    #     juni = DataCleaning_GovernmentBidsProfile.objects.order_by(sort_by)
                    else:
                        juni = DataCleaning_GovernmentBidsProfile.objects.exclude(state__exact='').exclude(
                            rfpkey__exact='').order_by(
                            sort_by)

            else:
                print("junaid1")
                if sort == 'due_date':
                    juni = DataCleaning_GovernmentBidsProfile.objects.filter(
                        due_date__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$').order_by(sort_by)
                elif sort == 'date_entered':
                    juni = DataCleaning_GovernmentBidsProfile.objects.filter(
                        date_entered__iregex='(\d{4})[/.-](\d{2})[/.-](\d{2})$').exclude(state__exact='').exclude(
                        rfpkey__exact='').exclude(rfpkey__isnull=True).order_by(sort_by)

                # elif sort == 'rfpkey':
                #     juni = DataCleaning_GovernmentBidsProfile.objects.order_by(sort_by)
                else:
                    juni = DataCleaning_GovernmentBidsProfile.objects.exclude(state__exact='').exclude(rfpkey__exact='').order_by(
                        sort_by)

            paginator = Paginator(juni, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
            items = paginator.count
            pages = paginator.num_pages

            res = {
                'totalItems': items,
                'totalPages': pages,
                'results': serializer.data,

            }
            return Response(res)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def category(request):
    if DataCleaning_GovernmentBidsProfile.objects.exists():
        if request.method == 'GET':
            uniqueCategory = DataCleaning_GovernmentBidsProfile.objects.all().distinct('category')[:10]
            serializers = CategorySerializer(uniqueCategory, many=True)
            print(serializers.data)
            return Response(serializers.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def allcategory(request):
    # if DataCleaning_GovernmentBidsProfile.objects.exists():
    try:
        results = RFPGurusMainCategory.objects.all()
        if request.method == 'GET':
            serializer_context = {'request': request}
            serializer = CategorySerializer(results, many=True, context=serializer_context)
            return Response(serializer.data)
    except:
        Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def states(request):
    if request.method == 'PUT':

        try:
            results = DataCleaning_GovernmentBidsProfile.objects.all().exclude(state__exact='').distinct('state')[:10]
            paginator = Paginator(results, 10)
            page = request.GET.get('page')
            serializer_context = {'request': request}
            serializer = StateSerializer(results, many=True, context=serializer_context)
            items = paginator.count
            res = {
                'Total Result': items,
                'Results': serializer.data

            }
            return Response(res)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def allcities(request,query):
    if request.method == 'GET':
        try:
            results = DataCleaning_GovernmentBidsProfile.objects.filter(state__contains=query).exclude(city__isnull=True).exclude(city__exact='').values('city').annotate(
                total=Count('city')).order_by('city')
            return Response({"Result": results})
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def allagencies(request):
    if request.method == 'GET':
        try:
            results = DataCleaning_GovernmentBidsProfile.objects.all().exclude(agency__isnull=True).exclude(agency__exact='').values('agency').annotate(
                total=Count('agency')).order_by('agency')
            print(results)
            return Response({"Result": results})
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def agencyData(request, query, items):
        if request.method == 'GET':
            try:
                items = int(items)

                results = DataCleaning_GovernmentBidsProfile.objects.filter(agency__contains=query).exclude(agency__exact='')
                paginator = Paginator(results, items)
                page = request.GET.get('page')
                try:
                    data = paginator.page(page)
                except PageNotAnInteger:
                    data = paginator.page(1)
                except EmptyPage:
                    data = paginator.page(paginator.num_pages)
                serializer_context = {'request': request}
                if request.user.id:
                    if Register.objects.get(user=request.user.id).is_subscribed:
                        serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)
                    else:
                        serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                else:
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                items = paginator.count
                pages = paginator.num_pages
                # serializer.data.update()
                res = {
                    'totalItems': items,
                    'totalPages': pages,
                    'Results': serializer.data

                }
                return Response(res)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def cityData(request, query, items):
        if request.method == 'GET':
            try:
                items = int(items)

                results = DataCleaning_GovernmentBidsProfile.objects.filter(city_or_county__contains=query).exclude(city_or_county__exact='')
                paginator = Paginator(results, items)
                page = request.GET.get('page')
                try:
                    data = paginator.page(page)
                except PageNotAnInteger:
                    data = paginator.page(1)
                except EmptyPage:
                    data = paginator.page(paginator.num_pages)
                serializer_context = {'request': request}
                if request.user.id:
                    if Register.objects.get(user=request.user.id).is_subscribed:
                        serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)
                    else:
                        serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                else:
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                items = paginator.count
                pages = paginator.num_pages
                # serializer.data.update()
                res = {
                    'totalItems': items,
                    'totalPages': pages,
                    'Results': serializer.data

                }
                return Response(res)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def allstates(request):
    if request.method == 'GET':
        try:
            results = RFPGurusStates.objects.all()
            serializer = stateSerializer(results, many=True)

            return Response({"Result": serializer.data})
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def stateData(request, query, items):
    if request.method == 'GET':
        try:
            items = int(items)
            results = DataCleaning_GovernmentBidsProfile.objects.filter(state__contains=query).exclude(state__exact='')
            paginator = Paginator(results, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            if request.user.id:
                print("id", request.user.id)
                if Register.objects.get(user=request.user.id).is_subscribed:
                    serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)
                    items = paginator.count
                    pages = paginator.num_pages

                    res = {
                        'totalItems': items,
                        'totalPages': pages,
                        'Results': serializer.data

                    }
                    return Response(res)

                else:
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                    items = paginator.count
                    pages = paginator.num_pages

                    res = {
                        'totalItems': items,
                        'totalPages': pages,
                        'Results': serializer.data

                    }
                    return Response(res)
            else:
                serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                items = paginator.count
                pages = paginator.num_pages
                # serializer.data.update()
                res = {
                    'totalItems': items,
                    'totalPages': pages,
                    'Results': serializer.data

                }
                return Response(res)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def unsubstateData(request, query, items):
    if request.method == 'GET':
        items = int(items)
        results = DataCleaning_GovernmentBidsProfile.objects.filter(state__contains=query).exclude(state__exact='')
        paginator = Paginator(results, items)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        serializer_context = {'request': request}
        serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
        items = paginator.count
        pages = paginator.num_pages

        res = {
            'totalItems': items,
            'totalPages': pages,
            'Results': serializer.data

        }
        return Response(res)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def categoryData(request, query, items):
    if request.method == 'GET':
        try:
            items = int(items)

            que = Q()
            for word in query.split():
                que &= Q(category__icontains=word)

            results = DataCleaning_GovernmentBidsProfile.objects.filter(que)
            #print (results)
            paginator = Paginator(results, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            #serializer_context = {'request': request}
            if request.user.id:
                print("id", request.user.id)
                if Register.objects.get(user=request.user.id).is_subscribed== True:

                    serializer = GovernmentBidsSerializersForSubscribers(data, many=True)
                    items = paginator.count
                    pages = paginator.num_pages

                    res = {
                        'totalItems': items,
                        'totalPages': pages,
                        'Results': serializer.data

                    }
                    return Response(res)

                elif(Register.objects.get(user=request.user.id).is_subscribed== False):

                    serializer = SubGovernmentBidsSerializers(data, many=True)

                    items = paginator.count
                    pages = paginator.num_pages

                    res = {
                        'totalItems': items,
                        'totalPages': pages,
                        'Results': serializer.data

                    }
                    return Response(res)
            else:
                serializer = SubGovernmentBidsSerializers(data, many=True)

                items = paginator.count
                pages = paginator.num_pages
                # serializer.data.update()
                res = {
                    'totalItems': items,
                    'totalPages': pages,
                    'Results': serializer.data

                }
                return Response(res)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def singlerfp(request,slug):
    print(slug)
    try:

        singledata = DataCleaning_GovernmentBidsProfile.objects.filter(seoTitleUrl=slug)
        print ("single",singledata)
        if singledata.exists():
            print(request.user.id)
            if request.user.id:
                if Register.objects.get(user=request.user.id).is_subscribed:
                    print(singledata)
                    serializer = GovernmentBidsSerializersForSubscribers(singledata, many=True)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    singledata = DataCleaning_GovernmentBidsProfile.objects.filter(seoTitleUrl=slug)
                    print(singledata)
                    serializer = SubGovernmentBidsSerializers(singledata, many=True)

                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                singledata = DataCleaning_GovernmentBidsProfile.objects.filter(seoTitleUrl=slug)
                print(singledata)
                serializer = SubGovernmentBidsSerializers(singledata, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        Response(status=status.HTTP_400_BAD_REQUEST)


def dateConversion(cu):
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
             'november', 'december']
    date = ''
    # cu = '2017-12-03T19:00:00.000Z'
    if len(cu) == 10:
        return str(cu)
    else:
        cu = str(cu).split('-', 3)
        date = cu[2][:2]
        print(date, cu)
        count = 0
        due_date = cu[0] + '-' + cu[1] + '-' + date
        print(due_date)
        return due_date


# @api_view(['PUT'])
# @permission_classes((permissions.AllowAny,))
# def filters(request, totalResult):
#     totalResult = int(totalResult)
#     current_time = timezone.now()
#     print("current time", current_time)
#     dt = str(current_time).split(' ', 2)
#     ar = dt[0].split('-', 3)
#     corrct =   str(ar[0]) + "/" + str(ar[1]) + "/" + str(ar[2])
#     end_date = ''
#     start_date = ''
#     # date_correct = "Wednesday, 15 November, 2017",
#     if request.method == 'PUT':
#         try:
#             results = DataCleaning_GovernmentBidsProfile.objects.all()
#             print ('resultsss   ', len(results))
#             check = True
#             for key, value in request.data.items():
#                 print('pairrrrrr   ',key, value)
#                 print('////////////////////')
#                 if (key == 'category' and value != 'empty'):
#                     que = Q()
#                     for word in value.split():
#                         print(word)
#                         que &= Q(category__icontains=word)
#                         print(que)
#                         # que = Q(title__icontains=query)
#                     print("Que", que)
#                     results = results.filter(que)
#                     print("Category ", len(results))
#                 elif (key == 'state' and value != 'empty'):
#                     results = results.filter(state__icontains=value)
#                     print("State ", len(results))
#                 elif key == 'status' and value == 'expire' and value != 'empty':
#                     results = results.filter(due_date__icontains='/')
#                     results = results.filter(due_date__lte=corrct)
#                 elif key == 'status' and value == 'active' and value != 'empty':
#                     print('Before' , results.count())
#                     results = results.filter(due_date__icontains='/')
#                     print('After', results.count())
#                     results = results.filter(due_date__gte=corrct)
#                 elif key == 'status' and value == 'all' and value != 'empty':
#                     # results = results.filter(due_date__icontains='/')
#                     results = results.all()
#                 elif key == 'posted_from' and value != 'empty':
#                     start_date = dateConversion(value)
#                     print("ddddddddddddddddddddddddddddddddddddddddstart_date", start_date)
#                 elif key == 'posted_to' and value != 'empty':
#                     end_date = dateConversion(value)
#                     print("dddddddddddddddddddddddddddddddddddddddd",end_date)
#             if len(end_date) > 8 and len(start_date) > 8:
#
#                 results = results.filter(due_date__icontains='/')
#                 results = results.filter(date_entered__icontains='/')
#                 results = results.filter(date_entered__range=(start_date, end_date))
#             print("Final Results" , results)
#             if (results.count()) == 0:
#                 Message = {"Result Not Found"}
#                 return Response(Message, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 try:
#                     print("Length " , (results.count()))
#                     if totalResult == 10:
#                         print("totalResult in if", totalResult)
#                         paginator = Paginator(results, totalResult)
#                     else:
#                         print("totalResult in else", totalResult)
#                         paginator = Paginator(results, totalResult)
#                 except:
#                     return Response(status=status.HTTP_400_BAD_REQUEST)
#                 print("totalResult in", totalResult)
#                 page = request.GET.get('page')
#                 try:
#                     data = paginator.page(page)
#                 except PageNotAnInteger:
#                     data = paginator.page(1)
#                 except EmptyPage:
#                     data = paginator.page(paginator.num_pages)
#                 serializer_context = {'request': request}
#                 print ('userrrr  ',request.user.id)
#                 # print ('subbbbbb   ',Register.objects.get(user=request.user).is_subscribed)
#                 if request.user.id!=None:
#                     try:
#                          if Register.objects.get(user=request.user.id).is_subscribed:
#                             serializer = GovernmentBidsSerializersForSubscribers(data, many=True,
#                                                                              context=serializer_context)
#                          else:
#                              serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
#
#                     except:
#                             serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
#                 else:
#                         serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
#
#                 items = paginator.count
#                 pages = paginator.num_pages
#                 res = {
#                     'TotalResult': items,
#                     'Total Pages': pages,
#                     'Results': serializer.data
#
#                 }
#                 return Response(res)
#         except:
#             Response(status=status.HTTP_400_BAD_REQUEST)
#



# Pure API

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def filters(request, totalResult):
    if request.method == 'PUT':
        print(request.data)
        totalResult = int(totalResult)
        current_time = timezone.now()
        print("current time", current_time)
        dt = str(current_time).split(' ', 2)
        ar = dt[0].split('-', 3)
        corrct = str(ar[0]) + "-" + str(ar[1]) + "-" + str(ar[2])
        end_date = ''
        start_date = ''
        que = Q()
        try:
            print(request['status'])
        except:
            print("Multidictionary")
        # date_correct = "Wednesday, 15 November, 2017",
        check = False
        ch = False
        try:
            for key, value in request.data.items():
                # for key in Filter:
                #     print('pairrrrrr   ', key, Filter[key])
                print('pairrrrrr   ', key, value)
                print('////////////////////')
                # value = Filter[key]
                if (key == 'category' and value == 'all'):
                    ch = True

                elif (key == 'category' and value is not None and value != 'all'):
                    for word in value.split():
                        print(word)
                        que &= Q(category__icontains=word)
                    check = True
                if (key == 'state' and value == 'all'):
                    ch = True

                elif (key == 'state' and value is not None and value != 'all'):
                    que &= Q(state__icontains=value)
                    check = True

                if (key == 'agency' and value == 'all'):
                  ch = True

                elif (key == 'agency' and value is not None and value !='all'):
                    que &= Q(agency__icontains = value)
                    check = True
                if (key == 'city' and value is not None):
                    que &= Q(city__icontains = value)
                    check = True

                if (key == 'status' and value == 'all'):
                     ch = True
                elif (key == 'status' and value == 'expire' and value is not None and value !='all'):

                    que &= Q(due_date__iregex='(\d{4})[-](\d{2})[-](\d{2})$')
                    que &= Q(due_date__lte=corrct)

                    check = True

                elif key == 'status' and value == 'active' and value is not None and value is not 'all':

                    que &= Q(due_date__iregex='(\d{4})[-](\d{2})[-](\d{2})$')
                    que &= Q(due_date__gte=corrct)
                    check = True

                if key == 'posted_from' and value is not None:
                    start_date = dateConversion(value)
                    print("ddddddddddddddddddddddddddddddddddddddddstart_date", start_date)
                if key == 'posted_to' and value is not None:
                    end_date = dateConversion(value)
                    print("dddddddddddddddddddddddddddddddddddddddd", end_date)
                if len(end_date) > 8 and len(start_date) > 8:
                # if str(end_date)[:-15] and str(start_date)[:-15]:
                    # results = results.filter(due_date__icontains='/')
                    # results = results.filter(date_entered__icontains='/')
                    # results = results.filter(date_entered__range=(start_date, end_date))
                    que &= Q()
                    que &= Q(due_date__icontains='-')
                    que &= Q(date_entered__range=(start_date, end_date))
                    check = True

                if (key == 'rfp_key' and value is not None):
                    que &= Q(rfpkey__icontains = value)
                    check = True

                if (key == 'title' and value is not None):
                    que &= Q(title__icontains = value)
                    check = True

            print(que)
            print("ch",ch )
            print("check",check )
            if (check==True) or (check==True and ch==True):
                results = DataCleaning_GovernmentBidsProfile.objects.filter(que).order_by(F('date_entered').desc(nulls_last=True))

            elif (ch==True)or(ch==True and check==False):
                results = DataCleaning_GovernmentBidsProfile.objects.all().order_by(F('date_entered').desc(nulls_last=True))


            if check or ch:
                if (results.count()) == 0:
                    Message = {"msg": "Result Not Found"}
                    return Response(Message, status=status.HTTP_404_NOT_FOUND)
                else:
                    try:
                        print("Length ", len(results))
                        if totalResult == 10:
                            print("totalResult in if", totalResult)
                            paginator = Paginator(results, totalResult)
                        else:
                            print("totalResult in else", totalResult)
                            paginator = Paginator(results, totalResult)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    print("totalResult in", totalResult)
                    page = request.GET.get('page')
                    try:
                        data = paginator.page(page)
                    except PageNotAnInteger:
                        data = paginator.page(1)
                    except EmptyPage:
                        data = paginator.page(paginator.num_pages)
                    serializer_context = {'request': request}
                    print('userrrr  ', request.user)
                    # print ('subbbbbb   ',Register.objects.get(user=request.user).is_subscribed)
                    if request.user.id:
                        try:
                            if Register.objects.get(user=request.user.id).is_subscribed:
                                serializer = GovernmentBidsSerializersForSubscribers(data, many=True,
                                                                                     context=serializer_context)
                            else:
                                serializer = GovernmentBidsSerializers(data, many=True, context=serializer_context)

                        except:
                            serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
                    else:
                        serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

                    items = paginator.count
                    pages = paginator.num_pages
                    res = {
                        'TotalResult': items,
                        'Total Pages': pages,
                        'Results': serializer.data

                    }
                    return Response(res)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def get_download_folder():
    home = os.path.expanduser("~")
    print(os.path.join(home, "Downloads"))
    return os.path.join(home, "Downloads")


def downloadFile(filename):
    try:
        print('Uplaod File')
        host = 'ns3101486.ip-54-36-177.eu'
        username = 'rfpgurus'
        password = 'rfp#231'
        port = 22

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Download
        ########

        remote_filepath = '/www/RFP_DATA/RFPMart/' + filename
        localpath = get_download_folder() + '/' + filename
        sftp.get(remote_filepath, localpath)

        sftp.close()
        transport.close()
        return True
    except:
        print("File Remove")
        return False


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def downloadFiles(request, filename):
    if request.method == 'GET':
        check = downloadFile(filename)
        if check == True:
            return Response({'msg': ' FILE DOWNLOAD'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def vendorsContacts(request):
    if request.method == 'GET':
        # try:
        print('///////////////////////////////////////////////////////////')
        results = VendorsContact.objects.all()
        serializer_context = {'request': request}
        serializer = ContactSeializer(results, many=True, context=serializer_context)
        res = {
            "Result": serializer.data
        }
        return Response(res, status=status.HTTP_200_OK)


# @api_view(['PUT'])
# def filters(request):
#     if request.method == 'PUT':
#         # results = DataCleaning_GovernmentBidsProfile.objects.all()
#
#         check = True
#         for key, value in request.data.items():
#             print(key, value)
#             print('////////////////////')
#             variable_column = key
#             search_type = 'contains'
#             check = False
#             if (key == 'category'):
#                 results = DataCleaning_GovernmentBidsProfile.objects.filter(category__icontains=value)
#                 print("Category ", len(results))
#                 continue
#             elif (key == 'state'):
#                 results = DataCleaning_GovernmentBidsProfile.objects.filter(state__icontains=value)
#                 print("State ", len(results))
#                 continue
#         if len(results) == 0:
#             Message = {"Result Not Found"}
#             return Response(Message, status=status.HTTP_404_NOT_FOUND)
#         else:
#             paginator = Paginator(results, 10)
#             page = request.GET.get('page')
#             try:
#                 data = paginator.page(page)
#             except PageNotAnInteger:
#                 data = paginator.page(1)
#             except EmptyPage:
#                 data = paginator.page(paginator.num_pages)
#             serializer_context = {'request': request}
#             serializer = GovernmentBidsSerializers(data, many=True, context=serializer_context)
#             items = paginator.count
#             pages = paginator.num_pages
#             res = {
#                 'TotalResult': items,
#                 'Total Pages': pages,
#                 'Results': serializer.data
#
#             }
#             return Response(res)

@api_view(['GET'])
def unsub_singlerfp(request, pk):
    if request.method == 'GET':
        if DataCleaning_GovernmentBidsProfile.objects.filter(id=pk).exists():
            singledata = DataCleaning_GovernmentBidsProfile.objects.filter(id=pk)
            print(singledata)
            serializer = SubGovernmentBidsSerializers(singledata, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response({'msg': ' Record not Get'}, status=status.HTTP_400_BAD_REQUEST)

            # return Response(serializer.data)

            #  serializer= DataCleaning_GovernmentBidsProfileSerializers(data=request.data)
            # title = serializer.validated_data['title']
            #  first_name = obj['first-name']
            #  last_name = obj['last-name']
            #  company = obj['company']
            #  email = obj['email']
            #  username = obj['username']
            #  password = obj['password']
            #  phone_no = obj['phone']
            #  about = obj['about']
            #
            #  print (username)
            #  print  (password)
            #  # user = User.
            #  user = User.objects.create_user(username = username, email = email,password= password, first_name = first_name, last_name= last_name)
            #  # user.save()
            #  register = Register(user=user,company=company,phone_no= phone_no, about_yourself= about)
            #  register.save();
            #  return Response({'msg': 'User Registered Successfully' }, status=status.HTTP_200_OK)


@api_view(['POST'])
def Contacts(request):
    if request.method == 'POST':
        try:
            print('///////////////////////////////////////////////////////////')
            name = None
            email = None
            phone = None
            message = None
            for key, value in request.data.items():
                if key == 'name':
                    name = value
                elif key == 'email':
                    email = value
                elif key == 'phone':
                    phone = value
                elif key == 'message':
                    message = value
            obj = Contact(name=name, email=email, phone=phone, message=message)
            obj.save()

            return Response({'msg': 'Message Success'}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def searchKeyword_raw(request,query, items):
    query="'"+query+"'"
    print("queryyy  ", query)
    print("item  ", items)
    res = {}
    if request.GET.get('page') == 1:
        offset = 0
        print("page 2 ", offset)
    else:
        offset = (int(request.GET.get('page')) * int(items)) - int(items)
        print("page 2 ", offset)
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) or "category" ~*  {1} or "state" ~*  {1} or "rfp_number" ~*  {1}'
    if (str(items) == '-1'):
        print("get all")

        main_data_query = 'Select {0} from rfp_governmentbidsprofile where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    else:
        print("not all")
        main_data_query = 'Select {0} from rfp_governmentbidsprofile  where  "tsv_title" @@ plainto_tsquery({1}) limit {2} offset {3}'
    # main_data_query = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where "title" ~* {1}'

    print('query  ')
    print(main_data_query)


    fields = [
             "id", "rfpkey", "rfp_number", "title","seoTitleUrl"
        ]
    out = ['"{0}"'.format(i) for i in fields]

    temp=[]
    extra_fields = []
    fields.extend(extra_fields)

    out.extend(['cast("{0}" as varchar)'.format(i) for i in extra_fields])

    if(int(items)!=-1):
        data_query = main_data_query.format(",".join(out), query, items, offset)
    else:
        data_query = main_data_query.format(",".join(out), query)


    # get_all_items = 'Select {0} from rfp_DataCleaning_GovernmentBidsProfile  where  "tsv_title" @@ plainto_tsquery({1}) offset 0'
    # get_all_data = get_all_items.format(",".join(out), query)


    print(data_query)
    f_count = len(fields)

    with connection.cursor() as cursor:
        cursor.execute(data_query)

        for i in cursor.fetchall():

            # if i[5] > 0:
            # print (i)
            current_item = {}
            for j in range(f_count):

                current_item[fields[j]] = i[j]

            temp.append(current_item)


        print("junaid")
        print(len(temp))
        print(len(temp)/int(items))
        res = {
            'totalItems': len(temp),
            'totalPages': 0,
            'results': temp

        }
        return Response(res,status=status.HTTP_200_OK)


# Get All Wish List RFP For Customers
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def UserWatchList(request):
    if request.method == 'GET':
        try:
            wish = UserWishlist.objects.filter(user=request.user)
            if not wish:
                return Response({'status': False,
                                 'message': 'No Rfp in your Watch List'},
                                status=status.HTTP_202_ACCEPTED)
        except UserWishlist.DoesNotExist:
            return Response({'status': False,
                             'message': 'No Rfp in your Watch List'},
                            status=status.HTTP_202_ACCEPTED)
        serializer = WishListSerializer(wish, many=True)
        data={
            'result':serializer.data,
            'total':wish.count()
        }
        return Response(data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        dic = request.data
        if not DataCleaning_GovernmentBidsProfile.objects.filter(pk=dic['rfp']).exists():
            return Response({'status': False,
                             'message': 'Invalid Rfp Name or Id'},
                            status=status.HTTP_202_ACCEPTED)

        rfpId = dic['rfp']
        if UserWishlist.objects.filter(user=request.user, wrfp=rfpId).exists():
            return Response({'status': False,
                             'message': 'This Rfp is already in your Watch List'},
                            status=status.HTTP_202_ACCEPTED)

        dic.update({"user": request.user.id})
        dic.update({"wrfp": DataCleaning_GovernmentBidsProfile.objects.filter(pk=dic['rfp'])})

        serializer = WishListPostSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            obj = serializer.save()
            if obj.id:
                wish = UserWishlist.objects.filter(user=request.user)
                print(wish)

                serializers = WishListSerializer(wish, many=True)
                data = {
                    'result': serializers.data,
                    'total': wish.count()
                }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def WatchlistDelete(request, rfpId):

    if request.method == 'DELETE':
        if UserWishlist.objects.filter(user=request.user, wrfp=rfpId).exists():
            checkout = UserWishlist.objects.filter(user=request.user, wrfp=rfpId)
            if not checkout:
                return Response({'status': False,
                                 'message': 'Not Found requested Item in your Watch List'},
                                status=status.HTTP_202_ACCEPTED)
            checkout.delete()
            return Response({'message': 'Deleted Finally', 'status': True}, status=status.HTTP_202_ACCEPTED)
        return Response({'status': False,
                         'message': 'Not Found requested Item in your Watch List'},
                        status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def Delete_all_watch_list(request):
    if request.method == 'DELETE':
        if UserWishlist.objects.filter(user=request.user).exists():
            checkout = UserWishlist.objects.filter(user=request.user)
            for i in checkout:
                i.delete()
            return Response({'message': 'All items Deleted', 'status': True}, status=status.HTTP_202_ACCEPTED)
        return Response({'status': False,
                         'message': 'No item in your watchlist'},
                        status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def dateupdate(request):
    if request.method == 'GET':
        list=DataCleaning_GovernmentBidsProfile.objects.all()

        for i in list:
            single=DataCleaning_GovernmentBidsProfile.objects.get(id=i.id)
            try:
             Adate = str(parser.parse(single.date_entered).strftime('%d' + '-' + '%b' + '-' + '%Y'))
            except:
                print('Remaining',single.id)
            single.new_date_entered=Adate
            single.save()
            print("date entered", single.date_entered)



            #DataCleaning_GovernmentBidsProfile.objects.filter(date_entered=single.date_entered).update(new_date_entered=Adate)

            print("after updation",single.new_date_entered)



    return Response(status=status.HTTP_200_OK)





@api_view(['GET'])
def getpreferencened(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        split = str(now)
        print(split)
        new=split[0:10]
        print ('new',new)
        list=[]
        user=Register.objects.get(id=265)
        prefer_state=user.state_preference
        prefer_city=user.city_preference
        prefer_county=user.county_preference
        prefer_agency=user.agency_preference
        prefer_category=user.user_preference

        if user.newsletter == True:
            que=Q()
            if user.state_preference is not None:
                for i in prefer_state:
                    que |= Q(state__icontains=i)
                    print("state",que)
            if user.city_preference is not None:
                for i in prefer_city:
                    que |= Q(city__icontains=i)
                    print("city", que)

            if user.county_preference is not None:
                for i in prefer_county:
                    que |= Q(city_or_county__icontains=i)
                    print("county", que)

            if user.agency_preference is not None:
                for i in prefer_agency:
                    que |= Q(agency__icontains=i)
                    print("agency", que)

            if user.user_preference is not None:
                for i in prefer_category:
                    que |= Q(category__icontains=i)
                    print("category", que)


            results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte='2018-11-26').filter(date_entered='2018-11-26').filter(que)
            serializers=GovernmentBids_emailSerializers(results,many=True)
            print(results)
            list.append(serializers.data)



        new = [x for x in list if x]

        flattened = [val for sublist in new for val in sublist]
        print("flattered",flattened)

        finalList = []

        for i in flattened:
            temp_d = dict(i)
            ls1 = temp_d.keys()
            ls2 = temp_d.values()
            finalList.append(dict(zip(ls1, ls2)))
        print('Dictionary>>>', finalList)
        key = {
            'list2': finalList,
        }

        # [i[0] for i in abc]
        # print(abc)
        message = get_template('emailAlert.html').render(key)
        email = EmailMessage('Latest RFPs from RFPGurus', message, to=['laraibshahid14@gmail.com'])
        email.content_subtype = 'html'
        email.send()
        print('mail sent')

        return Response(list)


@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        list=DataCleaning_GovernmentBidsProfile.objects.filter(date_entered__gte='2018-11-30').order_by(
            '-date_entered').exclude(date_entered__isnull=True).values()
        print(list)

@api_view(['GET'])
def test(request, items):

        if request.method == 'GET':
            items = int(items)
            now = datetime.datetime.now()
            split = str(now)
            print(split)


            week_ago1 = now - datetime.timedelta(days=7)
            week_ago=str(week_ago1)[0:11]

            print("week_ago",str(week_ago))
            query="SELECT * FROM public.rfp_datacleaning_governmentbidsprofile where date_entered <= '"+str(week_ago)+ "' ORDER BY date_entered DESC;"
            print("query",query)
            for p in DataCleaning_GovernmentBidsProfile.objects.raw(query):
             print("results",p)

            results=GovernmentBidsProfile.objects.filter(timestamp__range=[week_ago,split]).order_by('-date_entered').exclude(date_entered__isnull=True)
            results = DataCleaning_GovernmentBidsProfile.objects.filter(date_entered__gte=week_ago).order_by('-date_entered').exclude(date_entered__isnull=True)
            paginator = Paginator(p, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            if request.user.id:
                if Register.objects.get(user=request.user.id).is_subscribed:
                    serializer = GovernmentBidsSerializersForSubscribers(data, many=True, context=serializer_context)

                else:
                    serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)
            else:
                serializer = SubGovernmentBidsSerializers(data, many=True, context=serializer_context)

            items = paginator.count
            pages = paginator.num_pages
            res = {
                'totalItems': items,
                'totalPages': pages,
                'results': serializer.data

            }
            return Response(res)

        return Response(status=status.HTTP_400_BAD_REQUEST)
