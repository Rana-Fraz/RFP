import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from django.db import connection
from models import SubCategory
from rfp.models import GovernmentBidsProfile

cursor=connection.cursor()
cursor1=connection.cursor()
cursor2=connection.cursor()
cursor2=connection.cursor()
cursor.execute('SELECT (category) from public."rfp_governmentbidsprofile"')

cursor1.execute('SELECT COUNT(category) from public."rfp_governmentbidsprofile"')
data=cursor.fetchall()
print ('length...',len(data))
sub=SubCategory.objects.all()

lt=[]
for j in data:
    string=str(j)
    lt.append(string[2:-3])
    print(string[2:-3])

subdata=[]
for i in sub:
    var2=str(i)
    subdata.append(var2)
        #
for i in lt:
    for j in subdata:
        var1 = i.split()
        var2 = j.split()
        print(var1)
        print(var2)
        for k in var1:
            for l in var2:
                if (k == l)&(k!='and')&(k!='&')&(l!='and')&(l!='&')&(k!='services')&(l!='services')&(k!='equipment')&(l!='equipment')&(k!='management')&(l!='management')&(k!='supplies')&(l!='supplies')&(k!='hardware')&(l!='hardware'):

                    update=GovernmentBidsProfile.objects.filter(category=i)
                    update2=SubCategory.objects.filter(sub_category_name=j)
                    for m in update:
                        for o in update2:
                                    # print i.category
                            try:
                                cursor2.execute("UPDATE public.rfp_GovernmentBidsProfile SET sub_category_id ="+str( o.id)+"WHERE sub_category_id IS NULL and id="+str(m.id))
                                print("updated id",m.id)
                            except:
                                print("not",m.id)
                else:
                    print('not working')