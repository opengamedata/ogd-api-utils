import sys
sys.path.append('/var/www/wsgi-bin')
from flask import Flask
from apis.ClassroomAPI import ClassroomAPI
from apis.DashboardAPI import DashboardAPI
from apis.GameStateAPI import GameStateAPI
from apis.PlayerAPI import PlayerAPI

application = Flask(__name__)
application.secret_key = b'thisisafakesecretkey'

@application.route("/")
def home():
    return "Home"
    
ClassroomAPI.register(application)
DashboardAPI.register(application)
GameStateAPI.register(application)
PlayerAPI.register(application)

# if __name__ == '__main__':
# 	application.run(debug=True)