# import libraries
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
from typing import Any, Dict, List, Tuple, Union
# import locals
from config.config import settings
from ogd.core.interfaces.MySQLInterface import SQL

class QuestionnaireAPI:
    @staticmethod
    def register(app:Flask):
        # Expected WSGIScriptAlias URL path is /playerGameState
        api = Api(app)
        api.add_resource(QuestionnaireAPI.LoadQuestionnaire, '/load')

    class LoadQuestionnaire(Resource):
        def get(self):
            """GET request for a questionnaire
            Located at <server_addr>/questionnaires/load
            Requires 'player_id' and 'game_id'  as query string parameters.
            Optionally takes 'count' and 'offset' as query string parameters.
            Count controls the number of states to retrieve.
            Offset allows the retrieved states to be offset from the latest state.
                For example, count=1, offset=0 will retrieve the most recent state
                count=1, offset=1 will retrieve the second-most recent state

            :param game_id: A game id string.
            :type game_id: str
            :param player_id: A player id string.
            :type player_id: str
            :param session_id: A session id string.
            :type session_id: str
            :raises err: If a mysqlerror occurs, it will be raised up a level after setting an error message in the API call return value.
            :return: A dictionary containing a 'message' describing the result, and a 'state' containing either the actual state variable if found, else None
            :rtype: Dict[str, str | None]
            """
            ret_val = {
                "type":"GET",
                "val":None,
                "msg":"",
                "status":"SUCCESS",
            }

            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("game_id", type=str, required=True, location="args")
            parser.add_argument("player_id", type=str, required=True, location="args")
            parser.add_argument("session_id", type=str, required=True, location="args")
            args = parser.parse_args()

            game_id = args["game_id"]
            player_id = args["player_id"]
            session_id = args["session_id"]

            ret_val["val"] = json.dumps({
                "package_config_id": "somestring",
                "surveys": [
                    {
                        "display_event_id": "in-game event id",
                        "pages": [
                            {
                                "items": [
                                    {
                                        "prompt": "prompt to display to the user",
                                        "responses": [
                                            "responseA",
                                            "responseB",
                                            "responseC"
                                        ]
                                    },
                                    {
                                        "prompt": "second prompt label",
                                        "responses": [
                                            "responseA",
                                            "responseB",
                                            "responseC"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            })
            ret_val["msg"] = "Fake Questionnaire"

            return ret_val
