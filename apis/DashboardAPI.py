# Global imports
from datetime import datetime, timedelta
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
# Local imports
from config.config import settings
from ...opengamedata.games.WAVES.WaveExtractor import WaveExtractor
from ...opengamedata.interfaces.src.MySQLInterface import SQL, MySQLInterface
from ...opengamedata.interfaces.src.BigQueryInterface import BigQueryInterface
from ...opengamedata.managers.PopulationProcessor import PopulationProcessor
from ...opengamedata.managers.Request import Request, ExporterRange, ExporterFiles
from ...opengamedata.schemas.GameSchema import GameSchema
from ...opengamedata.schemas.TableSchema import TableSchema

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
            ret_val : Dict[str,Any] = {
                "type":"GET",
                "val":None,
                "msg":"",
                "status":"SUCCESS",
            }

            parser = reqparse.RequestParser()
            parser.add_argument("start_date")
            parser.add_argument("end_date")
            parser.add_argument("metrics")
            args = parser.parse_args()
            # set up interface and request
            interface = MySQLInterface("WAVES", settings=settings)
            # interface = BigQueryInterface(game_id=game_id, settings=settings)
            table_schema = TableSchema(schema_name="FIELDDAY_MYSQL", schema_path=Path("../schemas/TABLES"))
            _yesterday = datetime.now()-timedelta(days=1)
            _range = ExporterRange.FromDateRange(date_min=_yesterday, date_max=datetime.now(), source=interface)
            request = Request(interface=interface, range=_range, exporter_files=ExporterFiles())
            # set up population processor
            game_schema = GameSchema(schema_name="WAVES", schema_path=Path("../games/WAVES"))
            pop_processor = PopulationProcessor(ExtractorClass=WaveExtractor, game_schema=game_schema)
            # retrieve and process the data
            _dummy = request.RetrieveSessionIDs()
            sess_ids = _dummy if _dummy is not None else []
            _dummy = request._interface.RowsFromIDs(sess_ids)
            rows = _dummy if _dummy is not None else []
            try:
                for row in rows:
                    evt = table_schema.RowToEvent(row)
                    if evt.session_id in sess_ids:
                        pop_processor.ProcessEvent(evt)
                    else:
                        print(f"Found a session ({evt.session_id}) which was not in the list of sessions for processing.")
            except Exception as err:
                ret_val['msg'] = f"ERROR: Unknown error while processing data"
            else:
                cols = pop_processor.GetPopulationFeatureNames()
                vals = pop_processor.GetPopulationFeatures()
                ret_val['msg'] = "SUCCESS: Generated population features"
                ret_val["val"] = {cols[i] : vals[i] for i in range(min(len(cols), len(vals)))}
            return ret_val