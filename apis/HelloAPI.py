# Global imports
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
# Local imports
from config.config import settings

import sys
sys.path.append(settings["OGD_CORE_PATH"])
from interfaces.MySQLInterface import SQL

class HelloAPI:
    """API for logging and retrieving game states.
    Located at <server_addr>/player/<player_id>/game/<game_id>/state
    Valid requests are GET and POST.
    A GET request optionally takes 'count' and 'offset' as request parameters.
    A POST request should have a state variable as a request parameter.

    example usage:  GET fieldday-web.ad.education.wisc.edu/player/Bob/game/AQUALAB/state
                    with count=1, offset=0
    """
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(HelloAPI.Hello, '/hello')

    class Hello(Resource):
        def get(self):
            ret_val = {
                "message":"Hello! You GETted successfully!"
            }
            return ret_val

        def post(self):
            ret_val = {
							"message":"Hello! You POSTed successfully!"
						}
            return ret_val

        def put(self):
            ret_val = {
							"message":"Hello! You PUTted successfully!"
						}
            return ret_val