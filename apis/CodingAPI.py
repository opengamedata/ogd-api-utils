from flask import Flask, current_app
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
# import locals
from config.config import settings
from opengamedata.interfaces.MySQLInterface import SQL

class CodingAPI:
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
        api.add_resource(CodingAPI.CodeList, '/coding/game/<game_id>/codes')
        api.add_resource(CodingAPI.Code, '/coding/game/<game_id>/player/<player_id>/session/<session_id>/index/<index>/code/<code>/')

    class CodeList(Resource):
        def get(self, game_id:str):
            """GET request for a player's game state.
            Located at <server_addr>/player/<player_id>/game/<game_id>/state
            Optionally takes 'count' and 'offset' as request parameters.
            Count controls the number of states to retrieve.
            Offset allows the retrieved states to be offset from the latest state.
                For example, count=1, offset=0 will retrieve the most recent state
                count=1, offset=1 will retrieve the second-most recent state

            :param game_id: A game id string. Retrieved from <player_id> in the API request URL
            :type game_id: str
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
            ret_val['val'] = ["Code1", "Code2", "Code3"]
            ret_val['msg'] = f"SUCCESS: Got a (fake) list of codes for {game_id}"
            return ret_val

    class Code(Resource):
        def post(self, game_id, player_id, session_id, index, code):
            """POST request to store a player's game state.
            Located at <server_addr>/player/<player_id>/game/<game_id>/state
            Takes 'state' as request parameter.
            The state should be a string, encoding state in whatever way is convenient to the client program.
            No formatting of the string is enforced from the database side of things.

            :param player_id: A player id string. Retrieved from <player_id> in the API request URL
            :type player_id: str
            :param game_id: A game id string. Retrieved from <player_id> in the API request URL
            :type game_id: str
            :raises err: If a mysqlerror occurs, it will be raised up a level after setting an error message in the API call return value.
            :return: A dictionary containing a 'message' describing the result, and a 'state' containing either the actual state variable if found, else None
            :rtype: Dict[str, str | None]
            """            
            ret_val = {
                "type":"POST",
                "val":None,
                "msg":"",
                "status":"SUCCESS",
            }
            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("coder", type=str)
            parser.add_argument("notes", type=str)
            args = parser.parse_args()
            coder = args['coder']
            notes = args['notes']
            ret_val['msg'] = f"SUCCESS: Received code."
            current_app.logger.error(f"Got code through API:\ngame={game_id}, player_id={player_id}, session_id={session_id}, index={index}, code={code}, coder={coder}, notes={notes}")
            return ret_val