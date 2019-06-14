import os, django
# &(l!='equipment')&(l!='management')&(l!='supplies')&(l!='hardware')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from django.db import connection
from rfp.models import SubCategory
from category.models import Mapping

from rfp.models import GovernmentBidsProfile

cursor1=connection.cursor()
# cursor2=connection.cursor()

cursor1.execute('SELECT "govt_Category" FROM public.category_mapping ')

data1=cursor1.fetchall()

        #
for i in data1:
    # print (t[0]
    if(i[0]!=None):
        lower=i[0].lower()
        if (lower.find('services')>-1)|(lower.find('service')>-1):
            var1=lower.split()
            for l in var1:
                # print (l)
                if((l!='services')&(l!='service')):
                    obj=(' '+l+' ')

            # print (obj)
        else:
            obj=i[0]

        update=Mapping.objects.filter(govt_Category=i[0]).update(updated=obj)
        print ('BEFORE: ',i[0],'  AFTER:    ',obj)
