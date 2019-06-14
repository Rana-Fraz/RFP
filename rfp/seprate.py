from .models import DataCleaning_GovernmentBidsProfile,GovernmentBidsProfile
from .views import *
from django.db.models import Q
from core.models import User,Register
import datetime
from serializers import GovernmentBids_emailSerializers

def insertdata():
    count=0
    test = GovernmentBidsProfile.objects.values('seoTitleUrl', 'title','category')
    # print(clicktonextpage)
    # print(data)
    seonumber=46534456
    for match in test:
        filter = dict(match)
        Match = filter.get('seoTitleUrl')
        if Match == "":
            sco = str(filter.get('title'))

            count = count + 1
            #print("data",sco)
        #     if sco=="":
        #         cat=str(filter.get('category'))
        #         print(seoUrls(cat) + "-" + str(seonumber))
        #     else:
        #         print(seoUrls(sco) + "-" + str(seonumber))
        else:
            pass
        print(count)

#insertdata()


#
# from django.utils import timezone
# from django.contrib.sessions.models import Session
#
# def delete_all_unexpired_sessions_for_user(user):
#     unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     for session in unexpired_sessions:
#
#      if str(user) == session.get_decoded().get('_auth_user_id'):
#          session.delete()
#          print("deleted")





#delete_all_unexpired_sessions_for_user(363)

#sendNotification(209)

def alerts_for_expiration_rfp():
    dictionary = []
    dictionary1 = []
    dictionary2 = []
    dictionary3 = []
    dictionary4 = []
    now = datetime.datetime.now()
    split = str(now)
    print(split)
    new = split[0:10]
    print ('new', new)
    list = []
    user = Register.objects.get(id=294)
    prefer_state = user.state_preference
    prefer_city = user.city_preference
    prefer_county = user.county_preference
    prefer_agency = user.agency_preference
    prefer_category = user.user_preference

    if user.newsletter == True:
        que = Q()
        if user.state_preference is not None:
            for i in prefer_state:
                que |= Q(state__icontains=i)
               # print("state", que)
        if user.city_preference is not None:
            for i in prefer_city:
                que |= Q(city__icontains=i)
                #print("city", que)

        if user.county_preference is not None:
            for i in prefer_county:
                que |= Q(city_or_county__icontains=i)
                #print("county", que)

        if user.agency_preference is not None:
            for i in prefer_agency:
                que |= Q(agency__icontains=i)
               # print("agency", que)

        if user.user_preference is not None:
            for i in prefer_category:
                que |= Q(category__icontains=i)
                #print("category", que)

        results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte='2018-11-01').filter(
            que)
        serializers = GovernmentBids_emailSerializers(results, many=True)
        #print("queryset",serializers.data)
        list.append(serializers.data)

    new = [x for x in list if x]

    flattened = [val for sublist in new for val in sublist]
    #print("flattered", flattened)

    finalList = []

    for i in flattened:
        temp_d = dict(i)
        ls1 = temp_d.keys()
        ls2 = temp_d.values()
        demi=dict(zip(ls1, ls2))

        demo = demi.get('due_date')

        print("demo",demo)
        if demo != None:
            # Adate1 = parser.parse(demo).strftime('%Y' + '-' + '%m' + '-' + '%d')
            # Adate2 = parser.parse('2018-11-01').strftime('%Y' + '-' + '%m' + '-' + '%d')
            date_time_obj = datetime.datetime.strptime(demo, '%Y-%m-%d').date()
            print ("date_time_obj",date_time_obj)
            date_time_obj1 = datetime.datetime.strptime('2018-11-01', '%Y-%m-%d').date()
            print ("date_time_obj1", date_time_obj1)
            #demoo = demo- date_time_obj1
            demoo = date_time_obj-date_time_obj1
            print('Date>>>',demoo)
            # print('Due Date>>>',demo)
            # print('end date>>>',end_date)
            if demoo.days == 12:
                dictionary.append(demi)
            if demoo.days == 13:
                dictionary1.append(demi)
            if demoo.days == 11:
                dictionary2.append(demi)
            if demoo.days == 2:
                dictionary3.append(demi)
            if demoo.days == 0:
                dictionary4.append(demi)

    key = {
            'days15': dictionary,
            'days7': dictionary1,
            'days5': dictionary2,
            'days3': dictionary3,
            'days1': dictionary3
    }
    print("key",key)


    message = get_template('alertrfp.html').render(key)
    email = EmailMessage('Latest RFPs from RFPGurus', message, to=['laraib.shahid@brainplow.com'])
    email.content_subtype = 'html'
    email.send()
    print('mail sent')


alerts_for_expiration_rfp()

def demo():
    date_time_obj = datetime.datetime.strptime('2018-11-15', '%Y-%m-%d')
    date1=date_time_obj.isoformat()
    print ("date_time_obj",date1)
    date_time_obj1 = datetime.datetime.strptime('2018-11-01', '%Y-%m-%d')
    date2=date_time_obj1.isoformat()
    print ("date_time_obj1",date2)
    #demoo = demo- date_time_obj1
    demoo = date1-date2
    print('Date>>>',demoo)
#demo()