"""Module for the Population API code
"""
# import libraries
import os
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
# import 3rd-party libraries
from flask import Flask, current_app
from flask import request as flask_request
from flask_restful import Resource, Api
from flask_restful.inputs import datetime_from_iso8601
from flask_restful.reqparse import Argument, RequestParser
# import locals
from ogd.core.interfaces.DataInterface import DataInterface
from ogd.core.interfaces.outerfaces.DictionaryOuterface import DictionaryOuterface
from ogd.core.managers.ExportManager import ExportManager
from ogd.core.requests.Request import Request, ExporterRange
from ogd.core.requests.RequestResult import RequestResult
from ogd.core.schemas.ExportMode import ExportMode
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.schemas.configs.GameSourceSchema import GameSourceSchema
from ogd.core.schemas.games.GameSchema import GameSchema
from shared.schemas.ServerConfigSchema import ServerConfigSchema
from shared.utils.APIResult import APIResult, RESTType, ResultStatus
from shared.utils import APIUtils

class PopulationAPI:
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
        api.add_resource(PopulationAPI.PopulationMetrics, '/populations/metrics')
        api.add_resource(PopulationAPI.PopulationFeatureList, '/populations/metrics/list/<game_id>')
        PopulationAPI.ogd_core = server_settings.OGDCore
        PopulationAPI.ogd_config = core_settings

    class PopulationMetrics(Resource):
        """Class for handling requests for population-level features."""
        def post(self):
            """Handles a POST request for population-level features.
            Gives back a dictionary of the APIResult, with the val being a dictionary of columns to values for the given population.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            current_app.logger.info("Received population request.")
            ret_val = APIResult.Default(req_type=RESTType.POST)

            _game_id    : str      = "UNKOWN"
            _end_time   : datetime = datetime.now()
            _start_time : datetime = _end_time-timedelta(hours=1)

            # TODO: figure out how to make this use the default and print "help" part to server log, or maybe append to return message, instead of sending back as the only response from the server and dying here.
            parser = RequestParser()
            parser.add_argument(Argument(name="game_id",        location='form', type=str,                   required=True,  default=_game_id))
            parser.add_argument(Argument(name="start_datetime", location='form', type=datetime_from_iso8601, required=False, default=_start_time, nullable=True, help="Invalid starting date, defaulting to 1 hour ago."))
            parser.add_argument(Argument(name="end_datetime",   location='form', type=datetime_from_iso8601, required=False, default=_end_time,   nullable=True, help="Invalid ending date, defaulting to present time."))
            parser.add_argument(Argument(name="metrics",        location='form', type=str,                   required=False, default="[]",        nullable=True, help="Got bad list of metrics, defaulting to all."))
            try:
                current_app.logger.info(f"About to parse args from request with args='{flask_request.args}', and form='{flask_request.form}', body='{flask_request.data}'")
                args : Dict[str, Any] = parser.parse_args()

                _game_id    = args.get("game_id", _game_id)
                _end_time   = args.get('end_datetime', _end_time)
                _start_time = args.get('start_datetime', _start_time)
                _metrics    = APIUtils.parse_list(args.get('metrics') or "")

                result : RequestResult = RequestResult(msg="No Export")
                values_dict = {}
                # orig_cwd = os.getcwd()
                # os.chdir(PopulationAPI.ogd_core)

                _interface : Optional[DataInterface] = APIUtils.gen_interface(game_id=_game_id)
                if _metrics is not None and _interface is not None:
                    _range     = ExporterRange.FromDateRange(source=_interface, date_min=_start_time, date_max=_end_time)
                    _exp_types = {ExportMode.POPULATION}
                    _outerface = DictionaryOuterface(game_id=_game_id, config=GameSourceSchema.EmptySchema(), export_modes=_exp_types, out_dict=values_dict)
                    request    = Request(range=_range,         exporter_modes=_exp_types,
                                         interface=_interface, outerfaces={_outerface},
                                         feature_overrides=_metrics
                    )
                    # retrieve and process the data
                    current_app.logger.info(f"Processing population request {request}...")
                    export_mgr = ExportManager(config=PopulationAPI.ogd_config)
                    result = export_mgr.ExecuteRequest(request=request)
                    current_app.logger.info(f"Result: {result.Message}")
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                # os.chdir(orig_cwd)
            except Exception as err:
                ret_val.ServerErrored(f"Unknown error while processing Population request")
                current_app.logger.error(f"Got exception for Population request:\ngame={_game_id}\n{str(err)}\n{traceback.format_exc()}")
            else:
                current_app.logger.info(f"The values_dict:\n{values_dict}")
                cols = values_dict.get("populations", {}).get("cols", [])
                pop  = values_dict.get("populations", {}).get("vals", [[]])[0]
                ct = min(len(cols), len(pop))
                if ct > 0:
                    ret_val.RequestSucceeded(
                        msg="Generated population features",
                        val={cols[i] : pop[i] for i in range(ct)}
                    )
                else:
                    ret_val.RequestErrored("No valid population features")
            finally:
                return ret_val.ToDict()

    class PopulationFeatureList(Resource):
        """Class for getting a full list of features for a given game."""
        def get(self, game_id):
            """Handles a GET request for a list of sessions.

            :param game_id: _description_
            :type game_id: _type_
            :return: _description_
            :rtype: _type_
            """
            print("Received metric list request. confirm latest version")
            ret_val = APIResult.Default(req_type=RESTType.GET)

            try:
                feature_list = []
                # orig_cwd = os.getcwd()
                # os.chdir(PopulationAPI.ogd_core)

                _schema = GameSchema(game_id=game_id)
                for name,percount in _schema.PerCountFeatures.items():
                    if ExportMode.POPULATION in percount.Enabled:
                        feature_list.append(name)
                for name,aggregate in _schema.AggregateFeatures.items():
                    if ExportMode.POPULATION in aggregate.Enabled:
                        feature_list.append(name)
                # os.chdir(orig_cwd)
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing FeatureList request")
                print(f"Got exception for FeatureList request:\ngame={game_id}\n{str(err)}")
                print(traceback.format_exc())
            else:
                if feature_list != []:
                    ret_val.RequestSucceeded(msg="SUCCESS: Got metric list for given game", val=feature_list)
                else:
                    ret_val.RequestErrored("FAIL: Did not find any metrics for the given game")
            finally:
                return ret_val.ToDict()