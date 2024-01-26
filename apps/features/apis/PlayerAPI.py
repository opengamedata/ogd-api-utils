"""Module for the Player API code
"""
# import libraries
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union
# import 3rd-party libraries
from flask import Flask, Response, current_app
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import datetime_from_iso8601
# import locals
from ogd.core.interfaces.DataInterface import DataInterface
from ogd.core.interfaces.outerfaces.DictionaryOuterface import DictionaryOuterface
from ogd.core.managers.ExportManager import ExportManager
from ogd.core.requests.Request import Request, ExporterRange
from ogd.core.requests.RequestResult import RequestResult
from ogd.core.schemas.games.GameSchema import GameSchema
from ogd.core.schemas.IDMode import IDMode
from ogd.core.schemas.ExportMode import ExportMode
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.schemas.configs.GameSourceSchema import GameSourceSchema
from shared.schemas.ServerConfigSchema import ServerConfigSchema
from shared.utils.APIResult import APIResult, RESTType, ResultStatus
from shared.utils import APIUtils
class PlayerAPI:
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
        api.add_resource(PlayerAPI.PlayerList,        '/players/list/<game_id>')
        api.add_resource(PlayerAPI.PlayerFeatureList, '/players/metrics/list/<game_id>')
        api.add_resource(PlayerAPI.PlayersMetrics,    '/players/metrics')
        api.add_resource(PlayerAPI.PlayerMetrics,     '/player/metrics')
        PlayerAPI.ogd_core = server_settings.OGDCore
        PlayerAPI.ogd_config = core_settings

    class PlayerList(Resource):
        """Class for handling requests for a list of sessions over a date range."""
        def get(self, game_id) -> Response:
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            api_result = APIResult.Default(req_type=RESTType.GET)
            current_app.logger.info(f"Received request for {game_id} player list.")

            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            parser = reqparse.RequestParser()
            parser.add_argument("start_datetime", type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago.", location="args")
            parser.add_argument("end_datetime",   type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time.", location="args")
            args : Dict[str, Any] = parser.parse_args()

            _end_time   = args.get('end_datetime')   or _end_time
            _start_time = args.get('start_datetime') or _start_time

            try:
                result = {}
                # orig_cwd = os.getcwd()
                # os.chdir(PlayerAPI.ogd_core)
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _interface is not None:
                    _range = ExporterRange.FromDateRange(source=_interface, date_min=_start_time, date_max=_end_time)
                    result["ids"] = _range.IDs
                # os.chdir(orig_cwd)
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing PlayerList request")
                current_app.logger.error(f"Got exception for PlayerList request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = result.get('ids')
                if val is not None:
                    api_result.RequestSucceeded(msg="SUCCESS: Got ID list for given date range", val=val)
                else:
                    api_result.RequestErrored("FAIL: Did not find IDs in the given date range")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')

    class PlayersMetrics(Resource):
        """Class for handling requests for session-level features, given a list of session ids."""
        def post(self) -> Response:
            """Handles a POST request for session-level features for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            
            api_result = APIResult.Default(req_type=RESTType.GET)
            parser = reqparse.RequestParser()
            parser.add_argument("game_id",    location='form', type=str, required=True)
            parser.add_argument("player_ids", location='form', type=str, required=False, default="[]", nullable=True, help="Got bad list of player ids, defaulting to [].")
            parser.add_argument("metrics",    location='form', type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args = parser.parse_args()

            game_id = args["game_id"]
            
            current_app.logger.info(f"Received request for {game_id} players.")

            _metrics    = APIUtils.parse_list(args.get('metrics') or "")
            _player_ids = APIUtils.parse_list(args.get('player_ids') or "[]")
            try:
                result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}
                # orig_cwd = os.getcwd()
                # os.chdir(PlayerAPI.ogd_core)

                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _player_ids is not None and _interface is not None:
                    _range     = ExporterRange.FromIDs(source=_interface, ids=_player_ids, id_mode=IDMode.USER)
                    _exp_types = set([ExportMode.PLAYER])
                    _outerface = DictionaryOuterface(game_id=game_id, config=GameSourceSchema.EmptySchema(), export_modes=_exp_types, out_dict=values_dict)
                    request    = Request(interface=_interface,      range=_range,
                                         exporter_modes=_exp_types, outerfaces={_outerface},
                                         feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(config=PlayerAPI.ogd_config)
                    result = export_mgr.ExecuteRequest(request=request)
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                # os.chdir(orig_cwd)

            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing Players request")
                current_app.logger.error(f"Got exception for Players request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                val = values_dict.get("players")
                if val is not None:
                    api_result.RequestSucceeded(
                        msg="SUCCESS: Generated features for given sessions",
                        val=val
                    )
                else:
                    current_app.logger.debug(f"Couldn't find anything in result[players], result was:\n{result}")
                    api_result.RequestErrored("FAIL: No valid session features")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')
    
    class PlayerMetrics(Resource):
        """Class for handling requests for session-level features, given a session id."""
        def post(self) -> Response:
            """Handles a GET request for session-level features of a single Session.
            Gives back a dictionary of the APIResult, with the val being a dictionary of columns to values for the given player.

            :param game_id: _description_
            :type game_id: _type_
            :param player_id: _description_
            :type player_id: _type_
            :return: _description_
            :rtype: _type_
            """
            api_result = APIResult.Default(req_type=RESTType.GET)

            parser = reqparse.RequestParser()
            parser.add_argument("game_id",   location='form', type=str, required=True)
            parser.add_argument("player_id", location='form', type=str, required=True)
            parser.add_argument("metrics",   location='form', type=str, required=False, default="[]", nullable=True, help="Got bad list of metrics, defaulting to all.")
            args : Dict[str, Any] = parser.parse_args()

            game_id = args["game_id"]
            player_id = args["player_id"]

            current_app.logger.info(f"Received request for {game_id} player {player_id}.")
            current_app.logger.debug(f"Unparsed 'metrics' list from args: {args.get('metrics')}")

            _metrics = APIUtils.parse_list(args.get('metrics') or "")
            try:
                result : RequestResult = RequestResult(msg="Empty result")
                values_dict = {}
                
                # orig_cwd = os.getcwd()
                # os.chdir(PlayerAPI.ogd_core)

                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    _range = ExporterRange.FromIDs(source=_interface, ids=[player_id], id_mode=IDMode.USER)
                    current_app.logger.info(f"The range is {_range.IDs}")
                    _exp_types = set([ExportMode.PLAYER])
                    _outerface = DictionaryOuterface(game_id=game_id, config=GameSourceSchema.EmptySchema(), export_modes=_exp_types, out_dict=values_dict)
                    request    = Request(interface=_interface,      range=_range,
                                         exporter_modes=_exp_types, outerfaces={_outerface},
                                         feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    export_mgr = ExportManager(config=PlayerAPI.ogd_config)
                    result = export_mgr.ExecuteRequest(request=request)
                    current_app.logger.info(f"Result: {result.Message}")
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                # os.chdir(orig_cwd)
            except Exception as err:
                api_result.ServerErrored(f"ERROR: {type(err).__name__} error while processing Player request")
                current_app.logger.error(f"Got exception for Player request:\ngame={game_id}, player={player_id}\nerror={str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                current_app.logger.info(f"The values_dict:\n{values_dict}")
                cols   = values_dict.get("players", {}).get("cols", [])
                players = values_dict.get("players", {}).get("vals", [[]])
                player = self._findPlayer(player_list=players, target_id=player_id)
                ct = min(len(cols), len(player))
                if ct > 0:
                    api_result.RequestSucceeded(
                        msg="SUCCESS: Generated features for the given session",
                        val={cols[i] : player[i] for i in range(ct)}
                    )
                else:
                    current_app.logger.warn(f"Couldn't find anything in result[player], result was:\n{result}")
                    api_result.RequestErrored("FAIL: No valid session features")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')

        def _findPlayer(self, player_list, target_id):
            current_app.logger.info(f"The list of players is {player_list}")
            ret_val = None
            for _player in player_list:
                _player_id = _player[0]
                if _player_id == target_id:
                    ret_val = _player
            if ret_val is None:
                current_app.logger.warn(f"Didn't find {target_id} in list of player results, defaulting to first player in list (player ID={player_list[0]})")
                ret_val = player_list[0]
            return ret_val

    class PlayerFeatureList(Resource):
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
                
                # orig_cwd = os.getcwd()
                # os.chdir(PlayerAPI.ogd_core)

                _schema = GameSchema(game_id=game_id)
                for name,percount in _schema.PerCountFeatures.items():
                    if ExportMode.PLAYER in percount.Enabled:
                        feature_list.append(name)
                for name,aggregate in _schema.AggregateFeatures.items():
                    if ExportMode.PLAYER in aggregate.Enabled:
                        feature_list.append(name)
                # os.chdir(orig_cwd)
            except Exception as err:
                api_result.ServerErrored(f"ERROR: Unknown error while processing FeatureList request")
                current_app.logger.error(f"Got exception for FeatureList request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                if feature_list != []:
                    api_result.RequestSucceeded(msg="SUCCESS: Got metric list for given game", val=feature_list)
                else:
                    api_result.RequestErrored("FAIL: Did not find any metrics for the given game")
            finally:
                return Response(response=api_result.ToDict(), status=api_result.Status.value, mimetype='application/json')