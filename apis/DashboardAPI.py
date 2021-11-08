# Global imports
import logging
import os
import traceback
from datetime import datetime, timedelta
from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
# Local imports
from config.config import settings
from opengamedata.interfaces.MySQLInterface import MySQLInterface
from opengamedata.interfaces.BigQueryInterface import BigQueryInterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.managers.Request import Request, ExporterRange, ExporterTypes, ExporterLocations

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
            print("Received population request.")
            ret_val : Dict[str,Any] = {
                "type":"GET",
                "val":None,
                "msg":"",
                "status":"SUCCESS",
            }

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime", type=datetime, help="Invalid ending date, defaulting to present time.")
            parser.add_argument("metrics", help="Got bad list of metric, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()
            _start_time = args.get('start_datetime') or datetime.now()-timedelta(hours=1)
            _end_time   = args.get('end_datetime')   or datetime.now()
            print("Parsed args.")
            try:
                os.chdir("var/www/opengamedata/")
                # set up interface and request
                interface = MySQLInterface(game_id, settings=settings)
                print("Set up interface.")
                # interface = BigQueryInterface(game_id=game_id, settings=settings)
                # _range = ExporterRange.FromDateRange(date_min=_yesterday, date_max=datetime.now(), source=interface)
                _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=interface)
                _exp_types = ExporterTypes(events=False, sessions=False, population=True)
                _exp_locs = ExporterLocations(files=False, dict=True)
                print("Set up request params.")
                request = Request(interface=interface, range=_range, exporter_types=_exp_types, exporter_locs=_exp_locs)
                print("Set up request object.")
                # retrieve and process the data
                export_mgr = ExportManager(settings=settings)
                print("Set up export manager object.")
                result = export_mgr.ExecuteRequest(request=request, game_id=game_id)
                print("Ran export request.")
                os.chdir("../../../../")
            except Exception as err:
                ret_val['msg'] = f"ERROR: Unknown error while processing data"
                ret_val['status'] = "ERR_SRV"
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                cols = []
                vals = []
                if 'population' in result:
                    cols = result['population']['cols']
                    vals = result['population']['vals']
                ct = min(len(cols), len(vals))
                ret_val['msg'] = "SUCCESS: Generated population features"
                ret_val["val"] = {cols[i] : vals[i] for i in range(ct)}
            return ret_val