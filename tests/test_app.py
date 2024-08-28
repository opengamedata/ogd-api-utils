# import standard libraries
import sys, os
from logging.config import dictConfig
from typing import Any, Dict
# import 3rd-party libraries
from flask import Flask
# local imports
from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from src.ogd.apis.HelloAPI import HelloAPI

# By default we'll log to WSGI errors stream which ends up in the Apache error log
logHandlers : Dict[str, Any] = {
        'wsgi': { 
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream', 
            'formatter': 'default'
            }
    }

logRootHandlers = ['wsgi']

# If a dedicated log file is defined for this Flask app, we'll also log there
# Ensure this is a writable directory
if "OGD_FLASK_APP_LOG_FILE" in os.environ:
    logHandlers['wsgi_app_file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ["OGD_FLASK_APP_LOG_FILE"],
            'maxBytes': 100000000, # 100 MB
            'backupCount': 10, # Up to 10 rotated files
            'formatter': 'default'
    }

    logRootHandlers.append('wsgi_app_file')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': logHandlers,
    'root': {
        'level': 'INFO',
        'handlers': logRootHandlers
    }
})

application = Flask(__name__)

application.logger.setLevel('DEBUG')
application.secret_key = b'thisisafakesecretkey'

_cfg_elems = {
    "API_VERSION" : "APIUtilsTesting",
    "DEBUG_LEVEL" : "DEBUG"
}
_cfg = ServerConfigSchema(name="HelloAPITestServer", all_elements=_cfg_elems, logger=application.logger)

HelloAPI.register(app=application, server_config=_cfg)

# if __name__ == '__main__':
# 	application.run(debug=True)