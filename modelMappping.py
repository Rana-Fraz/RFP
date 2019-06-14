from fuzzywuzzy import process
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from django.db import connection
from rfp.models import SubCategory
from category.models import Mapping


cursor1=connection.cursor()

cursor1.execute('SELECT * FROM public.category_mapping')

data1=cursor1.fetchall()

sub=SubCategory.objects.all()


for i in data1:
    try:
        # print (i[4])
        obj=process.extractOne(i[4], sub)
        if(obj[1]>=70):
            # print (obj[1])

            update = SubCategory.objects.get(sub_category_name=obj[0])
            print (update)
            update1 = Mapping.objects.filter(govt_Category=i[4]).update(subcategory_name=update.sub_category_name, subcategory=update)
        else:
            update = SubCategory.objects.get(sub_category_name='uncategorized')
            print (update)
            update1 = Mapping.objects.filter(govt_Category=i[4]).update(subcategory_name=update.sub_category_name, subcategory=update)

    except:
        pass
