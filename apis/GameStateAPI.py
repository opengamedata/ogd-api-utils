import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
from config.config import settings

import sys
sys.path.append(settings["OGD_CORE_PATH"])
from interfaces.MySQLInterface import SQL

class GameStateAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(GameStateAPI.GameState, '/player/<player_id>/game/<game_id>/state')

    class GameState(Resource):
        def get(self, player_id, game_id):
            ret_val = {
                "states":None,
                "message":""
            }
            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("count", type=int, help="Invalid count of states to retrieve, default to 1.")
            parser.add_argument("offset", type=int, help="Invalid offset of states to retrieve, default to 0.")
            args = parser.parse_args()
            count = args['count'] if args['count'] is not None else 1
            offset = args['offset'] if args['offset'] is not None else 0
            # Step 2: get states from database.
            fd_config = settings["db_config"]["fd_users"]
            _dummy, db_conn = SQL.prepareDB(db_settings=fd_config)
            if db_conn is not None:
                query_string = f"SELECT `game_state` from {fd_config['DB_NAME']}.game_states\n\
                                 WHERE `player_id`=%s AND `game_id`=%s ORDER BY `save_time` DESC LIMIT %s, %s;"
                query_params = (player_id, game_id, offset, count)
                try:
                    states = SQL.Query(cursor=db_conn.cursor(), query=query_string, params=query_params, fetch_results=True)
            # Step 3: process and return states
                except MySQLError as err:
                    ret_val["message"] = "FAIL: Could not retrieve state(s), an error occurred!"
                    raise err
                else:
                    if len(states) == count:
                        ret_val["states"] = [state[0][0] for state in states],
                        ret_val["message"] = f"SUCCESS: Fake game state retrieved {count} states for your fake player ID: {player_id} and fake game {game_id}"
                    elif len(states) < count:
                        ret_val["message"] = f"FAIL: No {game_id} states were found for player {player_id}"
                    else: # len(states) > count
                        ret_val["message"] = f"FAIL: Error in retrieving states, to many states returned!"
                finally:
                    SQL.disconnectMySQL(db_conn)
            else:
                ret_val["message"] = "FAIL: Could not retrieve state(s), database unavailable!"
            return ret_val

        def post(self, player_id, game_id):
            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("state", type=str)
            args = parser.parse_args()
            state = args['state']
            # Step 2: insert state into database.
            fd_config = settings["db_config"]["fd_users"]
            _dummy, db_conn = SQL.prepareDB(db_settings=fd_config)
            if db_conn is not None:
                query_string = f"""INSERT INTO {fd_config['DB_NAME']}.game_states (`player_id`, `game_id`, `game_state`)
                                 VALUES (%s, %s, %s);"""
                query_params = (player_id, game_id, state)
                try:
                    SQL.Query(cursor=db_conn.cursor(), query=query_string, params=query_params, fetch_results=False)
                    db_conn.commit()
            # Step 3: Report status
                except MySQLError as err:
                    ret_val = { "message":"FAIL: Could not save state to the database, an error occurred!" }
                    raise err
                else:
                    ret_val = { "message": f"SUCCESS: Saved state to the database." }
                finally:
                    SQL.disconnectMySQL(db_conn)
            else:
                ret_val = { "message":"Could not save state, database unavailable!" }
            return ret_val