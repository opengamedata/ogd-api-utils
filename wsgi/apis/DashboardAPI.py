# Global imports
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
# Local imports
from config.config import settings

import sys
if not settings["OGD_CORE_PATH"] in sys.path:
    sys.path.append(settings["OGD_CORE_PATH"])
from ...opengamedata.interfaces.src.MySQLInterface import SQL, MySQLInterface
from ...opengamedata.interfaces.src.BigQueryInterface import BigQueryInterface
from ...opengamedata.managers.PopulationProcessor import PopulationProcessor
from ...opengamedata.games.WAVES.WaveExtractor import WaveExtractor
from ...opengamedata.schemas.GameSchema import GameSchema

class DashboardAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(DashboardAPI.Player, '/player/<player_id>/metrics')
        api.add_resource(DashboardAPI.Population, '/game/<game_id>/metrics')

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
    
    class Population(Resource):
        def get(self, game_id):
            parser = reqparse.RequestParser()
            parser.add_argument("start_date")
            parser.add_argument("end_date")
            parser.add_argument("metrics")
            args = parser.parse_args()
            interface = MySQLInterface("WAVES", )
            # pop_processor = PopulationProcessor()
            interface = BigQueryInterface(game_id=game_id, settings=settings)
            return {
								"metrics":{i:f"fake {i}" for i in args['metrics']},
                "message":f"Found these fake metrics for fake player {player_id}, for fake teacher {args['teacher_id']}"
            }