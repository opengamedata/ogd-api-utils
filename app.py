import sys
from flask import Flask
# Local imports
from config.config import settings
if not settings['OGD_CORE_PATH'] in sys.path:
    sys.path.append(settings['OGD_CORE_PATH'])

application = Flask(__name__)
application.logger.setLevel(settings['DEBUG_LEVEL'])
application.secret_key = b'thisisafakesecretkey'

def _logImportErr(msg:str, err:ImportError):
    application.logger.warning(msg)
    application.logger.exception(err)

try:
    from apis.ClassroomAPI import ClassroomAPI
except ImportError as err:
    _logImportErr(msg="Could not import Classroom API:", err=err)
else:
    ClassroomAPI.register(application)

try:
    from apis.DashboardAPI import DashboardAPI
except ImportError as err:
    _logImportErr(msg="Could not import Dashboard API:", err=err)
else:
    DashboardAPI.register(application)

try:
    from apis.PopulationAPI import PopulationAPI
except ImportError as err:
    _logImportErr(msg="Could not import Population API:", err=err)
else:
    PopulationAPI.register(application)

try:
    from apis.PlayerAPI import PlayerAPI
except ImportError as err:
    _logImportErr(msg="Could not import Player API:", err=err)
else:
    PlayerAPI.register(application)

try:
    from apis.SessionAPI import SessionAPI
except ImportError as err:
    _logImportErr(msg="Could not import Session API:", err=err)
else:
    SessionAPI.register(application)

try:
    from apis.GameStateAPI import GameStateAPI
except ImportError as err:
    _logImportErr(msg="Could not import GameState API:", err=err)
else:
    GameStateAPI.register(application)

try:
    from apis.HelloAPI import HelloAPI
except ImportError as err:
    _logImportErr(msg="Could not import Hello API:", err=err)
else:
    HelloAPI.register(application)

try:
    from apis.PlayerIDAPI import PlayerIDAPI
except ImportError as err:
    _logImportErr(msg="Could not import Player ID API:", err=err)
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