import sys
import logging
from flask import Flask
# Local imports
from config.config import settings
if not settings['OGD_CORE_PATH'] in sys.path:
    sys.path.append(settings['OGD_CORE_PATH'])

application = Flask(__name__)
application.logger.setLevel(logging.INFO)
application.secret_key = b'thisisafakesecretkey'

try:
    from apis.ClassroomAPI import ClassroomAPI
except ImportError as err:
    application.logger.warning("Could not import Classroom API", stack_info=True)
else:
    ClassroomAPI.register(application)

try:
    from apis.DashboardAPI import DashboardAPI
except ImportError as err:
    application.logger.warning("Could not import Dashboard API", stack_info=True)
else:
    DashboardAPI.register(application)

try:
    from apis.GameStateAPI import GameStateAPI
except ImportError as err:
    application.logger.warning("Could not import GameStateAPI API", stack_info=True)
else:
    GameStateAPI.register(application)

try:
    from apis.HelloAPI import HelloAPI
except ImportError as err:
    application.logger.warning("Could not import Hello API", stack_info=True)
else:
    HelloAPI.register(application)

try:
    from apis.PlayerAPI import PlayerAPI
except ImportError as err:
    application.logger.warning("Could not import Player API", stack_info=True)
else:
    PlayerAPI.register(application)

@application.route("/")
def home() -> str:
    """Defines a message when pinging the root of the API

    :return: The message for pinging API root.
    :rtype: str
    """
    return "Home"
    

# if __name__ == '__main__':
# 	application.run(debug=True)