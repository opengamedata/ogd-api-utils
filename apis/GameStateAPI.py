# import libraries
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
# import locals
from config.config import settings
from opengamedata.interfaces.MySQLInterface import SQL

class GameStateAPI:
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
        api.add_resource(GameStateAPI.GameState, '/player/<player_id>/game/<game_id>/state')

    class GameState(Resource):
        def get(self, player_id, game_id:str):
            """GET request for a player's game state.
            Located at <server_addr>/player/<player_id>/game/<game_id>/state
            Optionally takes 'count' and 'offset' as request parameters.
            Count controls the number of states to retrieve.
            Offset allows the retrieved states to be offset from the latest state.
                For example, count=1, offset=0 will retrieve the most recent state
                count=1, offset=1 will retrieve the second-most recent state

            :param player_id: A player id string. Retrieved from <player_id> in the API request URL
            :type player_id: str
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
            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("count", type=int, help="Invalid count of states to retrieve, default to 1.")
            parser.add_argument("offset", type=int, help="Invalid offset of states to retrieve, default to 0.")
            args = parser.parse_args()
            count = args['count'] if args['count'] is not None else 1
            offset = args['offset'] if args['offset'] is not None else 0
            # Step 2: get states from database.
            fd_config = settings["DB_CONFIG"]["fd_users"]
            tunnel, db_conn = SQL.ConnectDB(db_settings=fd_config)
            if db_conn is not None:
                query_string = f"SELECT `game_state` from {fd_config['DB_NAME']}.game_states\n\
                                 WHERE `player_id`=%s AND `game_id`=%s ORDER BY `save_time` DESC LIMIT %s, %s;"
                query_params = (player_id, game_id.upper(), offset, count)
                try:
                    states = SQL.Query(cursor=db_conn.cursor(), query=query_string, params=query_params, fetch_results=True)
            # Step 3: process and return states
                except MySQLError as err:
                    ret_val['msg'] = "FAIL: Could not retrieve state(s), an error occurred!"
                    ret_val['status'] = "ERR_DB"
                    raise err
                else:
                    if states is not None:
                        if len(states) == count:
                            ret_val['val'] = [str(state[0]) for state in states]
                            ret_val['msg'] = f"SUCCESS: Retrieved {len(ret_val['val'])} states."
                        elif len(states) < count:
                            ret_val['msg'] = f"FAIL: No {game_id} states were found for player {player_id}"
                            ret_val['status'] = "ERR_REQ"
                        else: # len(states) > count
                            ret_val['msg'] = f"FAIL: Error in retrieving states, too many states returned!"
                            ret_val['status'] = "ERR_SRV"
                    else:
                        ret_val['msg'] = f"FAIL: No {game_id} states could be retrieved"
                        ret_val['status'] = "ERR_DB"
                finally:
                    SQL.disconnectMySQL(db=db_conn)
            else:
                ret_val['status'] = "ERR_DB"
                ret_val['msg'] = "FAIL: Could not retrieve state(s), database unavailable!"
            return ret_val

        def post(self, player_id, game_id):
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
            parser.add_argument("state", type=str)
            args = parser.parse_args()
            state = args['state']
            # Step 2: insert state into database.
            fd_config = settings["DB_CONFIG"]["fd_users"]
            _dummy, db_conn = SQL.ConnectDB(db_settings=fd_config)
            if db_conn is not None:
                query_string = f"""INSERT INTO {fd_config['DB_NAME']}.game_states (`player_id`, `game_id`, `game_state`)
                                 VALUES (%s, %s, %s);"""
                query_params = (player_id, game_id, state)
                try:
                    SQL.Query(cursor=db_conn.cursor(), query=query_string, params=query_params, fetch_results=False)
                    db_conn.commit()
            # Step 3: Report status
                except MySQLError as err:
                    ret_val['msg'] = "FAIL: Could not save state to the database, an error occurred!"
                    ret_val['status'] = "ERR_DB"
                    raise err
                else:
                    ret_val['msg'] = "SUCCESS: Saved state to the database."
                finally:
                    SQL.disconnectMySQL(db_conn)
            else:
                ret_val['msg'] = "Could not save state, database unavailable!"
                ret_val['status'] = "ERR_DB"
            return ret_val