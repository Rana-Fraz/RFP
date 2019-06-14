# Zimbra Mail Server

import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth



def test_zimbra ():
    url = 'https://ns3031341.ip-149-202-94.eu/'
    comm = Communication(url)
    usr_token = auth.authenticate(
        url,
        'admin@rfpgurus.com',
        '123456'
    )

if __name__ == "__main__":
    test_zimbra()