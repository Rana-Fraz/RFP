from core.models import *
from rfp.models import *


def cites():
    list = GovernmentBidsProfile.objects.all().distinct('city')
    #print('list of agencies',list)
    for i in list:
        obj = City(name=i.city)
        obj.save()
        print('saved', i)

cites()


def cites_county():
    list = GovernmentBidsProfile.objects.all().distinct('city_or_county')
    #print('list of agencies',list)
    for i in list:
        obj = County(name=i.city_or_county)
        obj.save()
        print('saved', i)

cites_county()