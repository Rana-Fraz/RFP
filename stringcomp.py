from fuzzywuzzy import process
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from django.db import connection
from rfp.models import SubCategory
from rfp.models import GovernmentBidsProfile

# cursor1=connection.cursor()
#
# cursor1.execute('SELECT * from public."rfp_governmentbidsprofile"')
# data2=cursor1.fetchall()
# sub=SubCategory.objects.all()
#
# for i in data2:
#     try:
#         obj=(process.extractOne(i[5], sub))
#
#         update=SubCategory.objects.get(sub_category_name=obj[0])
#         update1=GovernmentBidsProfile.objects.filter(category=i[5]).update(sub_category=update)
#
#     except:
#         pass


# choices = ["pest control","fire fighting & rescue" ]
# # process.extract("new york jets", choices, limit=2)
# # [('New York Jets', 100), ('New York Giants', 78)]
# obj=process.extractOne("fire control equipment", choices)
# print (obj)
# ("Dallas Cowboys", 90)
file = open("RRRRRRRRRRRRRRRRRRRRRRR.txt", "w")
# obj = process.extractOne(i[0], sub)
# print (obj[0],' ',obj[1],'  ',i[0])
# if(obj[1]>=70):
# print (obj[1])
#     update = SubCategory.objects.get(sub_category_name=obj[0])
#     update1 = GovernmentBidsProfile.objects.filter(category=i[5]).update(sub_category=update,new_category_id=update.category_id)
file.write('obj[0]')