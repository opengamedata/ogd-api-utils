from flask import Flask
from flask_restful import Resource, Api, reqparse

class GameStateAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(GameStateAPI.GameState, '/player/<player_id>/state')

    class GameState(Resource):
        def get(self, player_id):
            return {
                "state":{"level":1,"time_played":120},
                "message":f"Fake game state retrieved for your fake player ID: {player_id}"
            }

        def post(self, player_id):
            parser = reqparse.RequestParser()
            parser.add_argument("state")
            parser.add_argument("game_id")
            args = parser.parse_args()
            return {
                "message":f"Fake saved the fake state {args['state']} for fake game {args['game_id']}, under fake player ID: {player_id}"
            }