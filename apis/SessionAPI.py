# import libraries
import json
import os
import traceback
from datetime import datetime, timedelta
from flask import Flask
from flask import current_app
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
from typing import Union
# import locals
from apis.APIResult import APIResult, RESTType, ResultStatus
from apis import APIUtils
from config.config import settings
from opengamedata.interfaces.DataInterface import DataInterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.schemas.Request import Request, ExporterRange, ExporterTypes, ExporterLocations, IDMode

class SessionAPI:
    """Class to define an API for the developer/designer dashboard"""
    @staticmethod
    def register(app:Flask):
        """Sets up the dashboard api in a flask app.

        :param app: _description_
        :type app: Flask
        """
        api = Api(app)
        api.add_resource(SessionAPI.SessionList, '/game/<game_id>/sessions/')
        api.add_resource(SessionAPI.Sessions, '/game/<game_id>/sessions/metrics')
        api.add_resource(SessionAPI.Session, '/game/<game_id>/session/<session_id>/metrics')

    
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
            _range : Union[ExporterRange, None] = None
            try:
                os.chdir("var/www/opengamedata/")
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(source=_interface, date_min=_start_time, date_max=_end_time)
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing SessionList request")
                current_app.logger.error(f"Got exception for SessionList request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                if _range is not None:
                    ret_val.RequestSucceeded(msg="SUCCESS: Got ID list for given date range", val=_range.IDs)
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
            parser.add_argument("session_ids", type=str, required=False, default="[]", nullable=True, help="Got bad list of session ids, defaulting to [].")
            parser.add_argument("metrics",    type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args = parser.parse_args()

            _metrics     = APIUtils.parse_list(args.get('metrics') or "")
            _session_ids = APIUtils.parse_list(args.get('session_ids') or "[]")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _session_ids is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(source=_interface, ids=_session_ids, id_mode=IDMode.SESSION)
                    _exp_types = ExporterTypes(events=False, sessions=True, players=False, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing Sessions request")
                current_app.logger.error(f"Got exception for Sessions request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = result.get('sessions')
                if val is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=val
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[sessions], result was:\n{result}")
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
            parser.add_argument("metrics", type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args = parser.parse_args()

            _metrics    = APIUtils.parse_list(args.get('metrics') or "")
            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(source=_interface, ids=[session_id], id_mode=IDMode.SESSION)
                    _exp_types = ExporterTypes(events=False, sessions=True, players=False, population=False)
                    _exp_locs = ExporterLocations(files=False, dict=True)
                    request = Request(interface=_interface, range=_range,
                                      exporter_types=_exp_types, exporter_locs=_exp_locs,
                                      feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(settings=settings)
                    result = export_mgr.ExecuteRequest(request=request)
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing Session request")
                current_app.logger.error(f"Got exception for Session request:\ngame={game_id}, player={session_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = result.get('sessions')
                if val is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val=val
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[session], result was:\n{result}")
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
