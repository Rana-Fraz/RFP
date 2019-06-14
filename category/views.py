# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from .models import *
from.serializers import *
from rfp.models import *
from django.db import connection
from PyDictionary import PyDictionary
from nltk.corpus import wordnet
from vocabulary.vocabulary import Vocabulary as vb
# Create vocabularyyour views here.
from collections import Counter

@api_view(['GET'])
def catget(request):
    if request.method == 'GET':
        # data=GovernmentBidsProfile.objects.all()
        # serializer=CategorySerilizer(data,many=True)
        # print (serializer.data)
        # return Response(data)
        cursor=connection.cursor()
        cursor1=connection.cursor()
        cursor2=connection.cursor()
        cursor.execute('SELECT (category) from public."rfp_governmentbidsprofile"')

        cursor1.execute('SELECT COUNT(category) from public."rfp_governmentbidsprofile"')
        data=cursor.fetchall()
        print 'length...',len(data)
        sub=SubCategory.objects.all()


        # for i in sub:
        #     print(i.sub_category_name.lower())

        lt=[]
        # lt=data

        for j in data:
            # print ('DATaaaaaloop..',str(j).lower())
            # var=str(j).lower().split()
            string=str(j)
            data1=string[3:-3].lower()
            # data1=data1.lower()
            lt.append(data1)
            # var.split("")
            # for k in var:
            #     print(k)
            #     lt.append(k)
        # lst=[]
        subdata=[]
        for i in sub:
            var2=i.sub_category_name.lower()
            subdata.append(var2)
            # for n in var2:
            #     lst.append(n)
            # big = [int(j) for j in str(var)]

            # value = len(var)
            #
            # for j in var:
            #     if (value < 12):
            #         var[value] = 'x'
            #     value = value + 1
            #
            #     lt.append()

                # if(i.sub_category_name.lower() == j):
                #     print(i.sub_category_name.lower())
                    # print(i.sub_category_name ,' ', j)
        #
        # print ('LENGTH>>>',len(data))
        # data_=str(data)[2:-2]
        # print ('dataaaaa',data)
        synonyms = []
        antonyms = []

        # vocabulary.meaning("life")
        # print(vb.synonym("grant"))
        # string1, string2 = "Abc def ghi", "def ghi abc"
        # print (Counter(string1.lower()) == Counter(string2.lower()))
        status=[]
        # for i in lt:
        #     print i
        file = open("newcomp.txt","w")
        for i in lt:
            for j in subdata:
                var1 = i.split()
                var2 = j.split()
                for k in var1:
                    for l in var2:
                        if (k == l)&(k!='and')&(k!='&')&(l!='and')&(l!='&')&(k!='services')&(l!='services')&(k!='equipment')&(l!='equipment')&(k!='management')&(l!='management')&(k!='supplies')&(l!='supplies')&(k!='hardware')&(l!='hardware'):
                            print i, ' ', j
                            print k, ' ', l
                            file.write(i)
                            file.write(" ")
                            file.write(j)
                            file.write("\n")
                            file.write(k)
                            file.write(" ")
                            file.write(l)
                            file.write("\n")
                            cursor2.execute('UPDATE public.GovernmentBidsProfile SET subcategory = Alfred Schmid WHERE subcategory IS NOT NULL ')

        file.close()

                # print i, j
                # status.append(obj)
                # if (i==j):
                #     obj = i,' = ',j
                #     # print True
                #     # print i,j
                #     status.append(obj)



        return Response(status)