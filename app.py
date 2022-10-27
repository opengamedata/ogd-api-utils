# import standard libraries
import sys
from logging.config import dictConfig
# import 3rd-party libraries
from flask import Flask

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

application = Flask(__name__)

# import locals
from config.config import settings
_ogd_core = settings['OGD_CORE_PATH']
if not _ogd_core in sys.path:
    sys.path.append(settings['OGD_CORE_PATH'])
    application.logger.info(f"Added {_ogd_core} to path.")

application.logger.setLevel(settings['DEBUG_LEVEL'])
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:Exception):
    application.logger.warning(msg)
    application.logger.exception(err)

try:
    from apis.ClassroomAPI import ClassroomAPI
except ImportError as err:
    _logImportErr(msg="Could not import Classroom API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Classroom API, general error:", err=err)
else:
    ClassroomAPI.register(application)

try:
    from apis.CodingAPI import CodingAPI
except ImportError as err:
    _logImportErr(msg="Could not import Coding API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Coding API, general error:", err=err)
else:
    CodingAPI.register(application)

try:
    from apis.DashboardAPI import DashboardAPI
except ImportError as err:
    _logImportErr(msg="Could not import Dashboard API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Dashboard API, general error:", err=err)
else:
    DashboardAPI.register(application)

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
    from apis.GameStateAPI import GameStateAPI
except ImportError as err:
    _logImportErr(msg="Could not import GameState API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import GameState API, general error:", err=err)
else:
    GameStateAPI.register(application)

try:
    from apis.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Hello API, general error:", err=err)
else:
    HelloAPI.register(application)

try:
    from apis.PlayerIDAPI import PlayerIDAPI
except ImportError as err:
    _logImportErr(msg="Could not import Player ID API:", err=err)
except Exception as err:
    _logImportErr(msg="Could not import Player ID API, general error:", err=err)
else:
    PlayerIDAPI.register(application)

@application.route("/")
def home() -> str:
    """Defines a message when pinging the root of the API

    :return: The message for pinging API root.
    :rtype: str
    """
    return "Home"
    
# if __name__ == '__main__':
# 	application.run(debug=True)