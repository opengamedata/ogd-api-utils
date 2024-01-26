"""Module for the Session API code
"""
# import libraries
import os
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Union
# import 3rd-party libraries
from flask import Flask, Response, current_app
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
# import locals
from ogd.core.interfaces.DataInterface import DataInterface
from ogd.core.interfaces.outerfaces.DictionaryOuterface import DictionaryOuterface
from ogd.core.managers.ExportManager import ExportManager
from ogd.core.requests.Request import Request, ExporterRange, IDMode
from ogd.core.requests.RequestResult import RequestResult
from ogd.core.schemas.ExportMode import ExportMode
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.schemas.configs.GameSourceSchema import GameSourceSchema
from ogd.core.schemas.games.GameSchema import GameSchema
from shared.schemas.ServerConfigSchema import ServerConfigSchema
from shared.utils.APIResult import APIResult, RESTType, ResultStatus
from shared.utils import APIUtils

class SessionAPI:
    """Class to define an API for the developer/designer dashboard"""

    ogd_core   : Path
    ogd_config : ConfigSchema

    @staticmethod
    def register(app:Flask, server_settings:ServerConfigSchema, core_settings:ConfigSchema):
        """Sets up the dashboard api in a flask app.

        :param app: _description_
        :type app: Flask
        """
        # Expected WSGIScriptAlias URL path is /data
        api = Api(app)
        api.add_resource(SessionAPI.SessionList, '/sessions/list/<game_id>')
        api.add_resource(SessionAPI.SessionsMetrics, '/sessions/metrics')
        api.add_resource(SessionAPI.SessionMetrics, '/session/metrics')
        api.add_resource(SessionAPI.SessionFeatureList, '/sessions/metrics/list/<game_id>')
        SessionAPI.ogd_core = server_settings.OGDCore
        SessionAPI.ogd_config = core_settings

    class SessionFeatureList(Resource):
        """Class for getting a full list of features for a given game."""
        def get(self, game_id) -> Response:
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            api_result = APIResult.Default(req_type=RESTType.GET)
            current_app.logger.info("Received metric list request.")

            try:
                feature_list = []

                _schema = GameSchema(game_id=game_id)
                for name,percount in _schema.PerCountFeatures.items():
                    if ExportMode.SESSION in percount.Enabled:
                        feature_list.append(name)
                for name,aggregate in _schema.AggregateFeatures.items():
                    if ExportMode.SESSION in aggregate.Enabled:
                        feature_list.append(name)
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing SessionFeatureList request")
                print(f"Got exception for SessionFeatureList request:\ngame={game_id}\n{str(err)}")
                print(traceback.format_exc())
            else:
                if feature_list != []:
                    api_result.RequestSucceeded(msg="SUCCESS: Got metric list for given game", val=feature_list)
                else:
                    api_result.RequestErrored("FAIL: Did not find any metrics for the given game")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')
    
    class SessionList(Resource):
        """Class for handling requests for a list of sessions over a date range."""
        def get(self, game_id) -> Response:
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info("Received session list request.")
            api_result = APIResult.Default(req_type=RESTType.GET)

        # 1. Set up variables and parser for Web Request
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.", location="args")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.", location="args")
            try:
        # 2. Perform actual variable parsing from Web Request
                args = parser.parse_args()

                _end_time   = args.get('end_datetime',   _end_time)
                _start_time = args.get('start_datetime', _start_time)
        # 3. Set up OGD Range based on data in Web Request
                _range : Union[ExporterRange, None] = None
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(source=_interface, date_min=_start_time, date_max=_end_time)
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing SessionList request")
                current_app.logger.error(f"Got exception for SessionList request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
        # 5. If range generation succeeded, get into return format and send back data.
                if _range is not None:
                    api_result.RequestSucceeded(msg="SUCCESS: Got ID list for given date range", val=_range.IDs)
                else:
                    api_result.RequestErrored("FAIL: Did not find IDs in the given date range")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')
    
    class SessionMetrics(Resource):
        """Class for handling requests for session-level features, given a session id."""
        def post(self) -> Response:
            """Handles a GET request for session-level features of a single Session.
            Gives back a dictionary of the APIResult, with the val being a dictionary of columns to values for the given session.

            :param game_id: _description_
            :type game_id: _type_
            :param session_id: _description_
            :type session_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info("Received session metrics request.")
            api_result = APIResult.Default(req_type=RESTType.GET)

        # 1. Set up variables and parser for Web Request
            _game_id    : str = "UNKOWN"
            _session_id : str = "UNKOWN"

            parser = reqparse.RequestParser()
            parser.add_argument("game_id", type=str, required=True)
            parser.add_argument("session_id", type=str, required=True)
            parser.add_argument("metrics", type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            try:
        # 2. Perform actual variable parsing from Web Request
                args = parser.parse_args()

                _game_id = args["game_id"]
                _session_id = args["session_id"]
                _metrics    = APIUtils.parse_list(args.get('metrics') or "")
        # 3. Set up OGD Request based on data in Web Request
                ogd_result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}

                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=_game_id)
                if _metrics is not None and _interface is not None:
                    _range      = ExporterRange.FromIDs(source=_interface, ids=[_session_id], id_mode=IDMode.SESSION)
                    _exp_types  = {ExportMode.SESSION}
                    _outerface  = DictionaryOuterface(game_id=_game_id, config=GameSourceSchema.EmptySchema(), export_modes=_exp_types, out_dict=values_dict)
                    ogd_request = Request(interface=_interface,      range=_range,
                                          exporter_modes=_exp_types, outerfaces={_outerface},
                                          feature_overrides=_metrics
                    )
        # 4. Run OGD with the Request
                    export_mgr = ExportManager(config=SessionAPI.ogd_config)
                    ogd_result = export_mgr.ExecuteRequest(request=ogd_request)
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing Session request")
                current_app.logger.error(f"Got exception for Session request:\ngame={_game_id}, player={_session_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
        # 5. If request succeeded, get into return format and send back data.
                cols = values_dict.get("sessions", {}).get("cols", [])
                sessions = values_dict.get("sessions", {}).get("vals", [[]])
                sess = self._findSession(session_list=sessions, target_id=_session_id)
                ct = min(len(cols), len(sess))
                if ct > 0:
                    api_result.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val={cols[i] : sess[i] for i in range(ct)}
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[session], result was:\n{ogd_result}")
                    api_result.RequestErrored("FAIL: No valid session features")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')

        def _findSession(self, session_list, target_id):
            ret_val = None
            for _session in session_list:
                _session_id = _session[0]
                if _session_id == target_id:
                    ret_val = _session
            if ret_val is None:
                current_app.logger.warn(f"Didn't find {target_id} in list of session results, defaulting to first session in list (session ID={session_list[0][0]})")
                ret_val = session_list[0]
            return ret_val

    class SessionsMetrics(Resource):
        """Class for handling requests for session-level features, given a list of session ids."""
        def post(self) -> Response:
            """Handles a POST  request for session-level features for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info("Received sessions request.")
            api_result = APIResult.Default(req_type=RESTType.POST)

        # 1. Set up variables and parser for Web Request
            _game_id     : str                 = "UNKOWN"
            _session_ids : Optional[List[str]] = None

            parser = reqparse.RequestParser()
            parser.add_argument("game_id", type=str, required=True)
            parser.add_argument("session_ids", type=str, required=False, default="[]", nullable=True, help="Got bad list of session ids, defaulting to [].")
            parser.add_argument("metrics",    type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            try:
        # 2. Perform actual variable parsing from Web Request
                args = parser.parse_args()

                _game_id = args.get("game_id", _game_id)
                _metrics     = APIUtils.parse_list(args.get('metrics') or "")
                _session_ids = APIUtils.parse_list(args.get('session_ids') or "[]")
                ogd_result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}
                
        # 3. Set up OGD Request based on data in Web Request
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=_game_id)
                if _metrics is not None and _session_ids is not None and _interface is not None:
                    _range      = ExporterRange.FromIDs(source=_interface, ids=_session_ids, id_mode=IDMode.SESSION)
                    _exp_types  = {ExportMode.SESSION}
                    _outerface  = DictionaryOuterface(game_id=_game_id, config=GameSourceSchema.EmptySchema(), export_modes=_exp_types, out_dict=values_dict)
                    ogd_request = Request(interface=_interface,      range=_range,
                                          exporter_modes=_exp_types, outerfaces={_outerface},
                                          feature_overrides=_metrics
                    )
        # 4. Run OGD with the Request
                    export_mgr = ExportManager(config=SessionAPI.ogd_config)
                    ogd_result = export_mgr.ExecuteRequest(request=ogd_request)
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing Sessions request")
                current_app.logger.error(f"Got exception for Sessions request:\ngame={_game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
        # 5. If request succeeded, get into return format and send back data.
                val = values_dict.get("sessions")
                if val is not None:
                    api_result.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=val
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[sessions], result was:\n{ogd_result}")
                    api_result.RequestErrored("FAIL: No valid session features")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')
