from fuzzywuzzy import process
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from django.db import connection
from rfp.models import SubCategory
from rfp.models import GovernmentBidsProfile

cursor1=connection.cursor()
# cursor2=connection.cursor()

cursor1.execute('SELECT distinct(category) FROM public.rfp_governmentbidsprofile')
# cursor2.execute('SELECT * FROM public.category_subcategory')





data1=cursor1.fetchall()

# data2=cursor2.fetchall()
sub=SubCategory.objects.all()

# print (data2[1])
file = open("testfile.txt", "w")
count=0
for i in data1:
    try:
        count=count+1
        # print (i[2:-2])
        # print (i[0])#id
        # print (i[1])#name
        obj=process.extractOne(i[0], sub)

        file.write(str(count))
        file.write('\t\t\t')

        file.write(str(obj[0]))
        file.write('\t\t\t')
        file.write(str(obj[1]))
        file.write('\t\t\t')
        file.write(str(i[0]))
        file.write('\n')
        # print (obj[0],' ',obj[1],'  ',i[0])
        # if(obj[1]>=70):
            # print (obj[1])
        #     update = SubCategory.objects.get(sub_category_name=obj[0])
        #     update1 = GovernmentBidsProfile.objects.filter(category=i[5]).update(sub_category=update,new_category_id=update.category_id)

            # else:
        #     update = SubCategory.objects.get(sub_category_name='uncategorized')
        #     update1 = GovernmentBidsProfile.objects.filter(category=i[5]).update(sub_category=update,new_category_id=update.category_id)

    except:
        pass
file.close()
