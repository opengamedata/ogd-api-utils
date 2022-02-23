# Global imports
import json
import logging
import os
import traceback
from datetime import datetime, timedelta
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
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
    
    @staticmethod
    def _parse_list(list_str:str):
        ret_val = None
        if ("[" in list_str) and ("]" in list_str):
            start = list_str.index("[")
            end   = list_str.index("]")
            ret_val = list_str[start+1:end].split(",")
        return ret_val

    class Player(Resource):
        def get(self, player_id):
            print("Received player request.")
            ret_val : Dict[str,Any] = {
                "type":"GET",
                "val":None,
                "msg":"",
                "status":"SUCCESS",
            }
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

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
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.")
            parser.add_argument("metrics",        type=str,                   required=False, default="[]",        nullable=True, help="Got bad list of metric, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()
            _start_time = args.get('start_datetime') or _start_time
            _end_time   = args.get('end_datetime')   or _end_time
            _metrics    = DashboardAPI._parse_list(args.get('metrics') or "")
            try:
                result = {}
                src_map = settings['GAME_SOURCE_MAP'].get(game_id)
                if _metrics is not None and src_map is not None:
                    os.chdir("var/www/opengamedata/")
                    # set up interface and request
                    if src_map['interface'] == "MySQL":
                        interface = MySQLInterface(game_id, settings=settings)
                        print(f"Using MySQLInterface for {game_id}")
                    elif src_map['interface'] == "BigQuery":
                        interface = BigQueryInterface(game_id=game_id, settings=settings)
                        print(f"Using BigQueryInterface for {game_id}")
                    else:
                        interface = MySQLInterface(game_id, settings=settings)
                        print(f"Could not find a valid interface for {game_id}, defaulting to MySQL!")
                    # _range = ExporterRange.FromDateRange(date_min=_yesterday, date_max=datetime.now(), source=interface)
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=interface)
                    _exp_types = ExporterTypes(events=False, sessions=False, population=True)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=interface, range=_range, exporter_types=_exp_types, exporter_locs=_exp_locs)
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request, game_id=game_id, feature_overrides=_metrics)
                    os.chdir("../../../../")
            except Exception as err:
                ret_val['msg'] = f"ERROR: Unknown error while processing data"
                ret_val['status'] = "ERR_SRV"
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                cols = []
                vals = []
                if result.get('population') is not None:
                    cols = [str(item) for item in result['population']['cols']]
                    vals = [str(item) for item in result['population']['vals']]
                    ct = min(len(cols), len(vals))
                    ret_val['msg'] = "SUCCESS: Generated population features"
                    ret_val["val"] = {cols[i] : vals[i] for i in range(ct)}
                else:
                    ret_val['msg'] = "FAIL: No valid population features"
                    ret_val['status'] = "ERR_REQ"
            return ret_val