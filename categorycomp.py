
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from rfp.models import GovernmentBidsProfile
from rfp.models import SubCategory


sub=SubCategory.objects.all()

for i in sub:
    try:
        update1=GovernmentBidsProfile.objects.filter(sub_category_id=i.id).exclude(sub_category_id__isnull=True).update(new_category_id=i.category.id)

    except:
        pass

