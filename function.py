from fuzzywuzzy import process
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from rfp.models import SubCategory



def categoryCompare(keyword):

    sub = SubCategory.objects.all()
    try:
        obj=process.extractOne(keyword, sub)

        if(obj[1]>=70):
            update = SubCategory.objects.get(sub_category_name=obj[0])
            subcategory=update.id
            category=update.category_id
        else:
            update = SubCategory.objects.get(sub_category_name='uncategorized')
            subcategory=update.id
            category=update.category_id

        return subcategory,category

    except:
        pass


print (categoryCompare(''))

