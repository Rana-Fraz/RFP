
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
django.setup()
from rfp.models import GovernmentBidsProfile
from rfp.models import SubCategory


# sub=SubCategory.objects.all()
#
# for i in sub:
#     try:
update1=GovernmentBidsProfile.objects.filter(agency="United States Trade and Development Agency").create(agency="UNITED STATES TRADE AND DEVELOPMENT AGENCY")

    # except:
    #     pass

