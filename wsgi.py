from flask import Flask
from apis.PlayerAPI import PlayerAPI
from apis.GameStateAPI import GameStateAPI

app = Flask(__name__)

@app.route("/")
def home():
	return "Home"

PlayerAPI.register(app)
GameStateAPI.register(app)

# if __name__ == '__main__':
# 	app.run(debug=True)