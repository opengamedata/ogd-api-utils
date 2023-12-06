# import standard libraries
import os
import logging
from logging.config import dictConfig
from typing import Any, Dict
# import 3rd-party libraries
from flask import Flask
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.utils.Logger import Logger
from shared.schemas.ServerConfigSchema import ServerConfigSchema

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
from shared.config.config import settings as srv_settings
from shared.config.coreconfig import settings as core_settings
_server_cfg = ServerConfigSchema(name="DataAppConfiguration", all_elements=srv_settings, logger=application.logger)
_core_cfg   = ConfigSchema(name="OGDConfiguration", all_elements=core_settings)

application.logger.setLevel(_server_cfg.DebugLevel)
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
    PopulationAPI.register(application, server_settings=_server_cfg, core_settings=_core_cfg)

try:
    from apis.PlayerAPI import PlayerAPI
except ImportError as err:
    _logImportErr(msg="Could not import Player API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Player API, general error:", err=err)
else:
    PlayerAPI.register(application, server_settings=_server_cfg, core_settings=_core_cfg)

try:
    from apis.SessionAPI import SessionAPI
except ImportError as err:
    _logImportErr(msg="Could not import Session API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Session API, general error:", err=err)
else:
    SessionAPI.register(application, server_settings=_server_cfg, core_settings=_core_cfg)

try:
    from shared.utils.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Hello API, general error:", err=err)
else:
    HelloAPI.register(application)
    
# if __name__ == '__main__':
# 	application.run(debug=True)