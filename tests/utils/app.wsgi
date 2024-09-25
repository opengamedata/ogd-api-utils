import sys, os
from pprint import pprint
from pathlib import Path
# import 3rd-party libraries
from flask import Flask

application = Flask(__name__)
application.logger.setLevel("INFO")
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:Exception):
    application.logger.warning(msg)
    application.logger.exception(err)

deploy_dir = "DEPLOY_DIR"
if not deploy_dir in sys.path:
    sys.path.insert(0, deploy_dir)
    sys.path.insert(0, str(Path(deploy_dir) / "ogd"))
try:
    from apis.schemas.ServerConfigSchema import ServerConfigSchema
    from apis.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API, an ImportError occurred:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Hello API, general error:", err=err)
else:
    _server_cfg_elems = {
        "API_VERSION" : "0.0.0-Testing",
        "DEBUG_LEVEL" : "DEBUG"
    }
    _server_cfg = ServerConfigSchema.FromDict(name="HelloAPITestServer", all_elements=_server_cfg_elems, logger=application.logger)
    HelloAPI.register(application, _server_cfg)

# if __name__ == '__main__':
# 	application.run(debug=True)