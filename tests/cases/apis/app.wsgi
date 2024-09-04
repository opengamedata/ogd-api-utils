import sys, os
from pathlib import Path
# import 3rd-party libraries
from flask import Flask

deploy_dir = "DEPLOY_DIR"
if not deploy_dir in sys.path:
    sys.path.insert(0, deploy_dir)
    sys.path.insert(0, str(Path(deploy_dir) / "ogd"))

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