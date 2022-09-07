"""Module for the Player API code
"""
# import libraries
import os
import traceback
from datetime import datetime, timedelta
from flask import Flask, current_app
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
from typing import Any, Dict, Optional, Union
# import locals
from apis.APIResult import APIResult, RESTType, ResultStatus
from apis import APIUtils
from config.config import settings
from opengamedata.interfaces.DataInterface import DataInterface
from opengamedata.interfaces.outerfaces.DictionaryOuterface import DictionaryOuterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.schemas.IDMode import IDMode
from opengamedata.schemas.ExportMode import ExportMode
from opengamedata.ogd_requests.Request import Request, ExporterRange
from opengamedata.ogd_requests.RequestResult import RequestResult

class PlayerAPI:
    """Class to define an API for the developer/designer dashboard"""
    @staticmethod
    def register(app:Flask):
        """Sets up the dashboard api in a flask app.

        :param app: _description_
        :type app: Flask
        """
        api = Api(app)
        api.add_resource(PlayerAPI.PlayerList, '/game/<game_id>/players/')
        api.add_resource(PlayerAPI.Players, '/game/<game_id>/players/metrics')
        api.add_resource(PlayerAPI.Player, '/game/<game_id>/player/<player_id>/metrics')

    class PlayerList(Resource):
        """Class for handling requests for a list of sessions over a date range."""
        def get(self, game_id):
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info(f"Received request for {game_id} player list.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.")
            args : Dict[str, Any] = parser.parse_args()

            _end_time   = args.get('end_datetime')   or _end_time
            _start_time = args.get('start_datetime') or _start_time

            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(source=_interface, date_min=_start_time, date_max=_end_time)
                    result["ids"] = _range.IDs
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing PlayerList request")
                current_app.logger.error(f"Got exception for PlayerList request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = result.get('ids')
                if val is not None:
                    ret_val.RequestSucceeded(msg="SUCCESS: Got ID list for given date range", val=val)
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
            current_app.logger.info(f"Received request for {game_id} players.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("player_ids", type=str, required=False, default="[]", nullable=True, help="Got bad list of player ids, defaulting to [].")
            parser.add_argument("metrics",    type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args = parser.parse_args()

            _metrics    = APIUtils.parse_list(args.get('metrics') or "")
            _player_ids = APIUtils.parse_list(args.get('player_ids') or "[]")
            try:
                result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}
                os.chdir("var/www/opengamedata/")
                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _player_ids is not None and _interface is not None:
                    _range     = ExporterRange.FromIDs(source=_interface, ids=_player_ids, id_mode=IDMode.USER)
                    _exp_types = set([ExportMode.PLAYER])
                    _outerface = DictionaryOuterface(game_id=game_id, out_dict=values_dict)
                    request    = Request(interface=_interface,      range=_range,
                                         exporter_modes=_exp_types, exporter_locs=[_outerface],
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
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing Players request")
                current_app.logger.error(f"Got exception for Players request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = values_dict.get("players")
                if val is not None:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=val
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[players], result was:\n{result}")
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()
    
    class Player(Resource):
        """Class for handling requests for session-level features, given a session id."""
        def get(self, game_id, player_id):
            """Handles a GET request for session-level features of a single Session.
            Gives back a dictionary of the APIResult, with the val being a dictionary of columns to values for the given player.

            :param game_id: _description_
            :type game_id: _type_
            :param player_id: _description_
            :type player_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info(f"Received request for {game_id} player {player_id}.")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("metrics", type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()

            current_app.logger.debug(f"Unparsed 'metrics' list from args: {args.get('metrics')}")
            _metrics = APIUtils.parse_list(args.get('metrics') or "")
            try:
                result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}
                os.chdir("var/www/opengamedata/")
                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(source=_interface, ids=[player_id], id_mode=IDMode.USER)
                    _exp_types = set([ExportMode.POPULATION])
                    _outerface = DictionaryOuterface(game_id=game_id, out_dict=values_dict)
                    request    = Request(interface=_interface,      range=_range,
                                         exporter_modes=_exp_types, exporter_locs=[_outerface],
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
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} error while processing Player request")
                current_app.logger.error(f"Got exception for Player request:\ngame={game_id}, player={player_id}\nerror={str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                cols   = values_dict.get("players", {}).get("cols", [])
                player = values_dict.get("players", {}).get("vals", [])[0]
                ct = min(len(cols), len(player))
                if ct > 0:
                    ret_val.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val={cols[i] : player[i] for i in range(ct)}
                    )
                else:
                    current_app.logger.warn(f"Couldn't find anything in result[player], result was:\n{result}")
                    ret_val.RequestErrored("FAIL: No valid session features")
            return ret_val.ToDict()