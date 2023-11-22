# import standard libraries
import os
import logging
import sys
from logging.config import dictConfig
# import 3rd-party libraries
from flask import Flask
from schemas.ServerConfigSchema import ServerConfigSchema
from opengamedata.utils.Logger import Logger

# By default we'll log to WSGI errors stream which ends up in the Apache error log
logHandlers = {
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
    try:
        flask_log_file = open(os.environ['OGD_FLASK_APP_LOG_FILE'], "a+")
    except FileNotFoundError:
        pass
    else:
        flask_log_file.close()
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

# import locals
from config.config import settings as srv_settings
_server_settings = ServerConfigSchema(name="DataAppConfiguration", all_elements=srv_settings, logger=application.logger)
if not _server_settings.OGDCore in sys.path:
    sys.path.append(str(_server_settings.OGDCore.absolute()))
    application.logger.info(f"Added {_server_settings.OGDCore} to path.")

application.logger.setLevel(_server_settings.DebugLevel)
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:Exception):
    application.logger.warning(msg)
    application.logger.exception(err)
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)

try:
    from apis.ClassroomAPI import ClassroomAPI
except ImportError as err:
    _logImportErr(msg="Could not import Classroom API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Classroom API, general error:", err=err)
else:
    ClassroomAPI.register(application)

try:
    from apis.PopulationAPI import PopulationAPI
except ImportError as err:
    _logImportErr(msg="Could not import Population API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Population API, general error:", err=err)
else:
    PopulationAPI.register(application)

try:
    from apis.PlayerAPI import PlayerAPI
except ImportError as err:
    _logImportErr(msg="Could not import Player API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Player API, general error:", err=err)
else:
    PlayerAPI.register(application)

try:
    from apis.SessionAPI import SessionAPI
except ImportError as err:
    _logImportErr(msg="Could not import Session API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Session API, general error:", err=err)
else:
    SessionAPI.register(application)

try:
    from utils.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Hello API, general error:", err=err)
else:
    HelloAPI.register(application)
    
# if __name__ == '__main__':
# 	application.run(debug=True)