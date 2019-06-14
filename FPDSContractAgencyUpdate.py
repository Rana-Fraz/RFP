
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from rfp.models import FPDS_DATA
from rfp.models import SubCategory


# sub=SubCategory.objects.all()
#
# for i in sub:
#     try:
update1=FPDS_DATA.objects.filter(contractingAgency="VETERANS AFFAIRS, DEPARTMENT OF").update(contractingAgency="DEPARTMENT OF VETERANS AFFAIRS")

    # except:
    #     pass

