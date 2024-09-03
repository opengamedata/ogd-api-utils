import sys, os
from logging.config import dictConfig
from typing import Any, Dict
# import 3rd-party libraries
from flask import Flask

if not "/var/www/wsgi-bin" in sys.path:
    sys.path.append("/var/www/wsgi-bin")

application = Flask(__name__)
application.logger.setLevel("INFO")
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:Exception):
    application.logger.warning(msg)
    application.logger.exception(err)

try:
    from ogd.apis.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API, an ImportError occurred:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Hello API, general error:", err=err)
else:
    HelloAPI.register(application)

# if __name__ == '__main__':
# 	application.run(debug=True)