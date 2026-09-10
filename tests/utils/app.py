from flask import Flask

application = Flask(__name__)
application.logger.setLevel("INFO")
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:Exception):
    application.logger.warning(msg)
    application.logger.exception(err)

try:
    from ogd.apis.configs.ServerConfig import ServerConfig
    from ogd.apis.HelloAPI import HelloAPI
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
    HelloAPI.register(application, _server_cfg, root_endpoint='hello')
