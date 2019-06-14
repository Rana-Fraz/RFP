from apscheduler.schedulers.background import BackgroundScheduler

from blog.models import Notification_Detail
from rfp.models import *
from rfp.serializers import *
from user_payment.models import *
import uuid
import authorize
from cryptography.fernet import Fernet
from core.models import Register,User
import datetime
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import get_template
scheduler = BackgroundScheduler()



def package_unsubmail():

    reg_obj = Register.objects.filter(is_subscribed=True)
    for r in reg_obj:
        user = User.objects.get(id=r.user.id)
        print("user detail",user)
        if r.is_subscribed == True:
            print("in subscription")
            date1 = datetime.datetime.now()
            date = str(date1)[0:10]
            auto = False
            card = PaymentCardInfo.objects.filter(user=user)
            for c in card:
                if c.autopay == True:
                    auto = True
                    print("auto pay card detail", c)

            if auto == False:
                exp = Payment.objects.filter(reg_fk=r)
                for i in exp:
                    if (i.is_expired == False):
                        if (date >= str(i.end_date)):
                            print("expired change values")
                            i.is_expired = True
                            i.save()
                            r.is_subscribed = False
                            r.save()
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






def autopay():
    id= 0
    reg_obj = Register.objects.filter(is_subscribed = True)
    for i in reg_obj:
        print("user_id",i.user.id)
        user = User.objects.get(id=i.user.id)
        print("user",user)
      #  if PaymentCardInfo.objects.get(autopay=True,user=user).exists():
        try:
         pay = PaymentCardInfo.objects.get(autopay=True,user=user)
         id=pay.id
         print("payment id",id)
        except:
            print("No payment info is null")
            print("No matching query")

        if id != 0:
            date1 = datetime.datetime.now()
            date = str(date1)[0:10]
            print("date",date)

            exp = Payment.objects.filter(reg_fk=i)
            print("payment matches",exp)
            for j in exp:
                if (j.is_expired == False):
                    print("false is true")
                    if (date >= str(j.end_date)):
                            print("expired change values")
                            j.is_expired = True
                            j.save()
                            i.is_subscribed = False
                            i.save()
                            user_id = Register.objects.get(id=i.id)
                            payment_fun(id,j.pkg_fk,user_id)
                            print("after function")

                else:
                        pass
        else:
            pass


def payment_fun(id,log_pkg_fk,user_id):
        pkg = Packages.objects.get(id=log_pkg_fk.id)
        detail = PaymentCardInfo.objects.get(id=id)
        print("detail", detail)
        exp = detail.expDate
        print("exp", exp)
        credit = detail.number[2:-5]
        cred = detail.number[-4:]

        info = detail.info[2:-1]
        cipher_suite = Fernet(bytes(info, 'utf8'))
        plain_text = cipher_suite.decrypt(bytes(credit, 'utf8'))
        plain_text1 = str(plain_text)
        number = plain_text1[2:-1] + cred

        creditno = number
        print("credit card ", creditno)
        c = detail.cvc[2:-1]

        cc = cipher_suite.decrypt(bytes(c, 'utf8'))
        code = str(cc)[2:-1]
        print("ccv", code)


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

            reg = Register.objects.get(id=user_id.id)
            print("getting user details",reg)
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
            print("sent email for successully auto pay ")









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
    reg = Register.objects.filter(newsletter=True)
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

        results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte=new).filter(
            que).exclude(title="").exclude(category="").exclude(state="").exclude(agency="").exclude(date_entered="").exclude(seoTitleUrl="")
        serializers = GovernmentBids_emailSerializers(results, many=True)
        #print("queryset",serializers.data)
        list.append(serializers.data)

        newlist = [x for x in list if x]

        flattened = [val for sublist in newlist for val in sublist]
        #print("flattered", flattened)

        # finalList = []
        if flattened:
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
                    date_time_obj1 = datetime.datetime.strptime(new, '%Y-%m-%d').date()
                    print ("date_time_obj1", date_time_obj1)
                    #demoo = demo- date_time_obj1
                    demoo = date_time_obj-date_time_obj1
                    print('Date>>>',demoo)
                    # print('Due Date>>>',demo)
                    # print('end date>>>',end_date)
                    if demoo.days == 14:
                        dictionary.append(demi)
                    if demoo.days == 6:
                        dictionary1.append(demi)
                    if demoo.days == 2:
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
                'days1': dictionary4
            }
            print("key",key)
            if dictionary or dictionary1 or dictionary2 or dictionary3 or dictionary4:
                message = get_template('alertrfp.html').render(key)
                email = EmailMessage('RFPs Alerts from RFPGurus', message, to=[a.user.email])
                email.content_subtype = 'html'
                email.send()
                print('Mail sent')
            else:
                print('No Date match')
        else:
            print('No Record Found')
    print('DONE')


def alerts_for_Subscribers():
    now = datetime.datetime.now()
    split = str(now)
    print(split)
    new = split[0:10]
    print ('new', new)
    list = []
    reg = Subscribers.objects.all()
    if reg != None:
        for a in reg:
            results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte=new).filter(
                date_entered=new).exclude(title="").exclude(category="").exclude(state="").exclude(agency="").exclude(date_entered="").exclude(seoTitleUrl="")
            serializers = GovernmentBids_emailSerializers(results, many=True)
            # print("queryset",serializers.data)
            list.append(serializers.data)
            new = [x for x in list if x]

            flattened = [val for sublist in new for val in sublist]
            print("flattered", flattened)
            finalList = []
            if flattened:
                for i in flattened:
                    temp_d = dict(i)
                    ls1 = temp_d.keys()
                    ls2 = temp_d.values()
                    finalList.append(dict(zip(ls1, ls2)))
            print('Dictionary>>>', finalList)
            key = {
                'list2': finalList,
            }
            if finalList:
                message = get_template('emailAlert.html').render(key)
                email = EmailMessage('Latest RFPs from RFPGurus', message, to=[a.user.email])
                email.content_subtype = 'html'
                email.send()
                print('mail sent')
            else:
                print('List Null')
        else:
            print('list Null')
    print('DONE')


def getpreferences():
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
    reg = Register.objects.filter(newsletter=True)
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
            que).exclude(title="").exclude(category="").exclude(state="").exclude(agency="").exclude(date_entered="").exclude(seoTitleUrl="")
        serializers = GovernmentBids_emailSerializers(results, many=True)
        #print("queryset",serializers.data)
        list.append(serializers.data)

        newlist = [x for x in list if x]

        flattened = [val for sublist in newlist for val in sublist]
        print("flattered",flattened)
        finalList = []
        if flattened:
            for i in flattened:
                temp_d = dict(i)
                ls1 = temp_d.keys()
                ls2 = temp_d.values()
                finalList.append(dict(zip(ls1, ls2)))
            print('Dictionary>>>', finalList)
            key = {
            'list2': finalList,
            }
            if dictionary or dictionary1 or dictionary2 or dictionary3 or dictionary4:
                message = get_template('emailAlert.html').render(key)
                email = EmailMessage('Latest RFPs from RFPGurus', message, to=[a.user.email])
                email.content_subtype = 'html'
                email.send()
                print('mail sent')
            else:
                print('List Null')
        else:
            print('list Null')
    print('DONE')



def sendNotification():

    user_reciver = User.objects.all()

    now = datetime.datetime.now()
    split = str(now)
    print(split)
    new = split[0:10]
    print ('new', new)

    for u in user_reciver:
        reg = Register.objects.filter(user=u,is_authenticated=True)
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

            if a.city_preference is not None:
                for i in prefer_city:
                    que |= Q(city__icontains=i)


            if a.county_preference is not None:
                for i in prefer_county:
                    que |= Q(city_or_county__icontains=i)


            if a.agency_preference is not None:
                for i in prefer_agency:
                    que |= Q(agency__icontains=i)


            if a.user_preference is not None:
                for i in prefer_category:
                    que |= Q(category__icontains=i)


            results = DataCleaning_GovernmentBidsProfile.objects.filter(timestamp__gte=new).filter(date_entered=new).filter(
                que).exclude(title="").exclude(agency="").exclude(seoTitleUrl="")


        if results is not None:
            for i in results:
                des='Check Out New RFP " '+i.title+'"'
                link=i.seoTitleUrl
                title=i.agency

                if Notification_Detail.objects.filter(description=des,receiver=u).exists():
                    print("Already exist")



                else:
                    Notification_Detail.objects.get_or_create(receiver=u,type_of_notification=title,description=des,target=link)









def start_job_for_notification():
    global job
    job = scheduler.add_job(sendNotification, 'interval', seconds=30)
    try:
        scheduler.start()
    except:
        pass





def start_job_for_Package_unSub():
    global job
    job = scheduler.add_job(package_unsubmail, 'interval', seconds=86400)
    try:
        scheduler.start()
    except:
        pass


def start_job_for_autopay():
    global job
    job = scheduler.add_job(autopay, 'interval', seconds=86400)
    try:
        scheduler.start()
    except:
        pass


def start_job_for_alerts_for_expiration_rfp():
    global job
    job = scheduler.add_job(alerts_for_expiration_rfp, 'interval', seconds=86400)
    try:
        scheduler.start()
    except:
        pass

def start_job_for_alerts_for_Subscribers():
    global job
    job = scheduler.add_job(alerts_for_Subscribers, 'interval', seconds=86400)
    try:
        scheduler.start()
    except:
        pass



def start_job_for_alerts():
    global job
    job = scheduler.add_job(getpreferences, 'interval', seconds=43200)
    try:
        scheduler.start()
    except:
        pass



# start_job_for_alerts_for_Subscribers()
# start_job_for_alerts_for_expiration_rfp()
# start_job_for_alerts()
# start_job_for_notification()
# start_job_for_autopay()
# start_job_for_Package_unSub()