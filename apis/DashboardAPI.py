# Global imports
import json
import os
import traceback
from datetime import datetime, timedelta
from flask import Flask
from flask import current_app
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
# Local imports
from config.config import settings
from apis.APIResult import APIResult, RESTType, ResultStatus
from opengamedata.interfaces.MySQLInterface import MySQLInterface
from opengamedata.interfaces.BigQueryInterface import BigQueryInterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.managers.Request import Request, ExporterRange, ExporterTypes, ExporterLocations
from opengamedata.schemas.GameSchema import GameSchema

class DashboardAPI:
    """Class to define an API for the developer/designer dashboard"""
    @staticmethod
    def register(app:Flask):
        """Sets up the dashboard api in a flask app.

        :param app: _description_
        :type app: Flask
        """
        api = Api(app)
        api.add_resource(DashboardAPI.FeatureList, '/game/<game_id>/metrics/list')
        api.add_resource(DashboardAPI.Population, '/game/<game_id>/metrics')
        api.add_resource(DashboardAPI.PlayerList, '/game/<game_id>/players/')
        api.add_resource(DashboardAPI.Players, '/game/<game_id>/players/metrics')
        api.add_resource(DashboardAPI.Player, '/game/<game_id>/player/<player_id>/metrics')
        api.add_resource(DashboardAPI.SessionList, '/game/<game_id>/sessions/')
        api.add_resource(DashboardAPI.Sessions, '/game/<game_id>/sessions/metrics')
        api.add_resource(DashboardAPI.Session, '/game/<game_id>/session/<session_id>/metrics')
    
    @staticmethod
    def parse_list(list_str:str) -> Union[List[Any], None]:
        """Simple utility to parse a string containing a bracketed list into a Python list.

        :param list_str: _description_
        :type list_str: str
        :return: _description_
        :rtype: Union[List[Any], None]
        """
        ret_val = None
        if ("[" in list_str) and ("]" in list_str):
            start = list_str.index("[")
            end   = list_str.index("]")
            ret_val = list_str[start+1:end].split(",")
        return ret_val

    @staticmethod
    def gen_interface(game_id):
        """Utility to set up an Interface object for use by the API, given a game_id.

        :param game_id: _description_
        :type game_id: _type_
        :return: _description_
        :rtype: _type_
        """
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

    class FeatureList(Resource):
        """Class for getting a full list of features for a given game."""
        def get(self, game_id):
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            print("Received metric list request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            try:
                feature_list = []
                os.chdir("var/www/opengamedata/")
                _schema = GameSchema(schema_name=f"{game_id}.json")
                for name,percount in _schema.percount_features().items():
                    if percount.get('enabled', False):
                        feature_list.append(name)
                for name,aggregate in _schema.aggregate_features().items():
                    if aggregate.get('enabled', False):
                        feature_list.append(name)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while attempting to get metric list")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if feature_list != []:
                    ret_val.RequestSucceeded(msg="SUCCESS: Got metric list for given game", val=feature_list)
                else:
                    ret_val.RequestErrored("FAIL: Did not find any metrics for the given")
            return ret_val.ToDict()

    class Population(Resource):
        """Class for handling requests for population-level features."""
        def get(self, game_id):
            """Handles a GET request for population-level features.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info("Received population request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            # TODO: figure out how to make this use the default and print "help" part to server log, or maybe append to return message, instead of sending back as the only response from the server and dying here.
            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.")
            parser.add_argument("metrics",        type=str,                   required=False, default="[]",        nullable=True, help="Got bad list of metric, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()

            _end_time   = args.get('end_datetime')   or _end_time
            _start_time = args.get('start_datetime') or _start_time
            _metrics    = DashboardAPI.parse_list(args.get('metrics') or "")
            current_app.logger.debug(f"Metrics list received from request: {_metrics}")

            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=_interface)
                    _exp_types = ExporterTypes(events=False, sessions=False, players=False, population=True)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
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

    class PlayerList(Resource):
        """Class for handling requests for a list of sessions over a date range."""
        def get(self, game_id):
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
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
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=_interface)
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

    class Players(Resource):
        """Class for handling requests for session-level features, given a list of session ids."""
        def get(self, game_id):
            """Handles a GET request for session-level features for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            print("Received session request.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("player_ids")
            parser.add_argument("metrics")
            args = parser.parse_args()

            _metrics     = DashboardAPI.parse_list(args.get('metrics') or "")
            _player_ids = DashboardAPI.parse_list(args.get('player_ids') or "[]")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _player_ids is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(ids=_player_ids, source=_interface)
                    _exp_types = ExporterTypes(events=False, sessions=False, players=True, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=result['sessions']
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    
    class Player(Resource):
        """Class for handling requests for session-level features, given a session id."""
        def get(self, game_id, player_id):
            """Handles a GET request for session-level features of a single Session.

            :param game_id: _description_
            :type game_id: _type_
            :param session_id: _description_
            :type session_id: _type_
            :return: _description_
            :rtype: _type_
            """
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("metrics")
            args = parser.parse_args()

            _metrics    = DashboardAPI.parse_list(args.get('metrics') or "")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(ids=[player_id], source=_interface)
                    _exp_types = ExporterTypes(events=False, sessions=False, players=True, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val=result['sessions']
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    
    class SessionList(Resource):
        """Class for handling requests for a list of sessions over a date range."""
        def get(self, game_id):
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
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
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(date_min=_start_time, date_max=_end_time, source=_interface)
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
        """Class for handling requests for session-level features, given a list of session ids."""
        def get(self, game_id):
            """Handles a GET request for session-level features for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
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
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _session_ids is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(ids=_session_ids, source=_interface)
                    _exp_types = ExporterTypes(events=False, sessions=True, players=False, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=result['sessions']
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    
    class Session(Resource):
        """Class for handling requests for session-level features, given a session id."""
        def get(self, game_id, session_id):
            """Handles a GET request for session-level features of a single Session.

            :param game_id: _description_
            :type game_id: _type_
            :param session_id: _description_
            :type session_id: _type_
            :return: _description_
            :rtype: _type_
            """
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("metrics")
            args = parser.parse_args()

            _metrics    = DashboardAPI.parse_list(args.get('metrics') or "")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface = DashboardAPI.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(ids=[session_id], source=_interface)
                    _exp_types = ExporterTypes(events=False, sessions=True, players=False, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing data")
                print(f"Got exception: {str(err)}")
                print(traceback.format_exc())
            else:
                if result.get('sessions') is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val=result['sessions']
                    )
                else:
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    