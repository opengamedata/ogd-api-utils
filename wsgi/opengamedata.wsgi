import sys
if not "/var/www/wsgi-bin" in sys.path:
    sys.path.append('/var/www/wsgi-bin')
if not "/var/www/opengamedata" in sys.path:
    sys.path.append('/var/www/opengamedata')
from app import application