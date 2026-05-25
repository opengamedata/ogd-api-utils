import sys
import site
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

# 1. Add local directory to path, so we can import locals.
HOME_FOLDER = "DEPLOY_DIR"
if not HOME_FOLDER in sys.path:
    sys.path.insert(0, HOME_FOLDER)
    sys.path.insert(0, str(Path(HOME_FOLDER) / "ogd"))

# 2. Set up venv
py_version = ".".join([str(sys.version_info.major), str(sys.version_info.minor)])
packages_dir = Path(HOME_FOLDER) / ".venv" / "lib" / f"python{py_version}" / "site-packages"

site.addsitedir(str(packages_dir))
sys.path.insert(0, sys.path.pop()) # Move venv sitedir to front of sys.path

# 3. Register api
try:
    from apis.configs.ServerConfig import ServerConfig
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
    _server_cfg = ServerConfig.FromDict(name="HelloAPITestServer", unparsed_elements=_server_cfg_elems)
    HelloAPI.register(application, _server_cfg)

# if __name__ == '__main__':
# 	application.run(debug=True)