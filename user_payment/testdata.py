import os
# from rfp.models import *
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RFPGurus.settings")
# django.setup()
# test=GovernmentsBidsUser.objects.get_or_create(
#     profile_url=str("test")
# )
import time

import requests


def Cloud():
    my_url = 'https://storage.rfpgurus.com/'
    path1 = r'/home/laraib/Desktop/imagesrfpgurus/rfppgurus/States'
    filename = os.listdir(path1)
    for f in filename:
        print('urlllllllll   ', f)

        userdata = {'path': 'image/', 'filename': f}


        files = {'file': open(path1 + '/' + f, "rb")}

        r = requests.post(my_url, files=files, params=userdata,
                            verify=False)
        time.sleep(10)
        print('https://storage.rfpgurus.com/bplrfpgurus/' + f)
            #global icloud_path
            #icloud_path = 'https://storage.rfpgurus.com/bplrfpgurus/' + firstname + str(
            #    name) + '.zip'


Cloud()