import sys
from flask import Flask
# Local imports
from config.config import settings
if not settings['OGD_CORE_PATH'] in sys.path:
    sys.path.append(settings['OGD_CORE_PATH'])
from apis.ClassroomAPI import ClassroomAPI
from apis.DashboardAPI import DashboardAPI
from apis.GameStateAPI import GameStateAPI
from apis.HelloAPI import HelloAPI
from apis.PlayerAPI import PlayerAPI

application = Flask(__name__)
application.secret_key = b'thisisafakesecretkey'

@application.route("/")
def home():
    return "Home"
    
ClassroomAPI.register(application)
DashboardAPI.register(application)
GameStateAPI.register(application)
HelloAPI.register(application)
PlayerAPI.register(application)

# if __name__ == '__main__':
# 	application.run(debug=True)