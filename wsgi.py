from flask import Flask
from apis.ClassroomAPI import ClassroomAPI
from apis.DashboardAPI import DashboardAPI
from apis.GameStateAPI import GameStateAPI
from apis.PlayerAPI import PlayerAPI

app = Flask(__name__)

@app.route("/")
def home():
	return "Home"

ClassroomAPI.register(app)
DashboardAPI.register(app)
GameStateAPI.register(app)
PlayerAPI.register(app)

# if __name__ == '__main__':
# 	app.run(debug=True)