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
from apis.APIResult import APIResult, RESTType, ResultStatus
from opengamedata.interfaces.MySQLInterface import MySQLInterface
from opengamedata.interfaces.BigQueryInterface import BigQueryInterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.managers.Request import Request, ExporterRange, ExporterTypes, ExporterLocations

class DashboardAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(DashboardAPI.Population, '/game/<game_id>/metrics')
        api.add_resource(DashboardAPI.SessionList, '/game/<game_id>/sessions/')
        api.add_resource(DashboardAPI.Sessions, '/game/<game_id>/sessions/metrics')
        api.add_resource(DashboardAPI.Session, '/game/<game_id>/session/<session_id>/metrics')
    
    @staticmethod
    def parse_list(list_str:str) -> Union[List[Any], None]:
        ret_val = None
        if ("[" in list_str) and ("]" in list_str):
            start = list_str.index("[")
            end   = list_str.index("]")
            ret_val = list_str[start+1:end].split(",")
        return ret_val

    @staticmethod
    def gen_interface(game_id):
        ret_val = None
        src_map = settings['GAME_SOURCE_MAP'].get(game_id)
        if src_map is not None:
            # set up interface and request
            if src_map['interface'] == "MySQL":
                ret_val = MySQLInterface(game_id, settings=settings)
                print(f"Using MySQLInterface for {game_id}")
            elif src_map['interface'] == "BigQuery":
                ret_val = BigQueryInterface(game_id=game_id, settings=settings)
                print(f"Using BigQueryInterface for {game_id}")
            else:
                ret_val = MySQLInterface(game_id, settings=settings)
                print(f"Could not find a valid interface for {game_id}, defaulting to MySQL!")
        return ret_val

    class Population(Resource):
        def get(self, game_id):
            print("Received population request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.")
            parser.add_argument("metrics",        type=str,                   required=False, default="[]",        nullable=True, help="Got bad list of metric, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()

            _end_time   = args.get('end_datetime')   or _end_time
            _start_time = args.get('start_datetime') or _start_time
            _metrics    = DashboardAPI.parse_list(args.get('metrics') or "")

            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and interface is not None:
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=interface)
                    _exp_types = ExporterTypes(events=False, sessions=False, population=True)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=interface, range=_range, exporter_types=_exp_types, exporter_locs=_exp_locs)
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request, game_id=game_id, feature_overrides=_metrics)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('population') is not None:
                    cols = [str(item) for item in result['population']['cols']]
                    vals = [str(item) for item in result['population']['vals']]
                    ct = min(len(cols), len(vals))
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated population features",
                        val={cols[i] : vals[i] for i in range(ct)}
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid population features")
            return ret_val.ToDict()

    class SessionList(Resource):
        def get(self, game_id):
            print("Received session list request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.")
            args = parser.parse_args()

            _end_time   = args.get('end_datetime')   or _end_time
            _start_time = args.get('start_datetime') or _start_time
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                interface = DashboardAPI.gen_interface(game_id=game_id)
                if interface is not None:
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=interface)
                    result["ids"] = _range.GetIDs()
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('ids') is not None:
                    ret_val.RequestSucceeded(msg="SUCCESS: Got ID list for given date range", val=result['ids'])
                else:
                    ret_val.RequestErrored("FAIL: Did not find IDs in the given date range")
            return ret_val.ToDict()

    class Sessions(Resource):
        def get(self, game_id):
            print("Received session request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("session_ids")
            parser.add_argument("metrics")
            args = parser.parse_args()

            _metrics     = DashboardAPI.parse_list(args.get('metrics') or "")
            _session_ids = DashboardAPI.parse_list(args.get('session_ids') or "[]")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _session_ids is not None and interface is not None:
                    _range = ExporterRange.FromIDs(ids=_session_ids, source=interface)
                    _exp_types = ExporterTypes(events=False, sessions=True, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=interface, range=_range, exporter_types=_exp_types, exporter_locs=_exp_locs)
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request, game_id=game_id, feature_overrides=_metrics)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    cols = [str(item) for item in result['population']['cols']]
                    vals = [str(item) for item in result['population']['vals']]
                    ct = min(len(cols), len(vals))
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val={cols[i] : vals[i] for i in range(ct)}
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    
    class Session(Resource):
        def get(self, game_id, session_id):
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("metrics")
            args = parser.parse_args()

            _metrics    = DashboardAPI.parse_list(args.get('metrics') or "")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and interface is not None:
                    _range = ExporterRange.FromIDs(ids=[session_id], source=interface)
                    _exp_types = ExporterTypes(events=False, sessions=True, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=interface, range=_range, exporter_types=_exp_types, exporter_locs=_exp_locs)
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request, game_id=game_id, feature_overrides=_metrics)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    cols = [str(item) for item in result['population']['cols']]
                    vals = [str(item) for item in result['population']['vals']]
                    ct = min(len(cols), len(vals))
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val={cols[i] : vals[i] for i in range(ct)}
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    