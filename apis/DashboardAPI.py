from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection

class DashboardAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(DashboardAPI.Player, '/player/<player_id>/metrics')

    class Player(Resource):
        def get(self, player_id):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            parser.add_argument("metrics")
            args = parser.parse_args()
            return {
								"metrics":{i:f"fake {i}" for i in args['metrics']},
                "message":f"Found these fake metrics for fake player {player_id}, for fake teacher {args['teacher_id']}"
            }