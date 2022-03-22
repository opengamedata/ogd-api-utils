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
from apis import APIUtils
from config.config import settings
from apis.APIResult import APIResult, RESTType, ResultStatus
from opengamedata.interfaces.DataInterface import DataInterface
from opengamedata.managers.ExportManager import ExportManager
from opengamedata.schemas.GameSchema import GameSchema
from opengamedata.schemas.Request import Request, ExporterRange, ExporterTypes, ExporterLocations

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
                ret_val.ServerErrored(f"ERROR: Unknown error while processing FeatureList request")
                print(f"Got exception for FeatureList request:\ngame={game_id}\n{str(err)}")
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
            _metrics    = APIUtils.parse_list(args.get('metrics') or "")
            current_app.logger.debug(f"Metrics list received from request: {args.get('metrics')}")
            current_app.logger.debug(f"Metrics list parsed: {_metrics}")

            try:
                result = {}
                os.chdir("var/www/opengamedata/")
                _interface : Union[DataInterface, None] = APIUtils.gen_interface(game_id=game_id)
                if _metrics is not None and _interface is not None:
                    current_app.logger.debug(f"Made it into clause for doing request.")
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
                elif _metrics is None:
                    current_app.logger.warning("_metrics was None")
                elif _interface is None:
                    current_app.logger.warning("_interface was None")
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: Unknown error while processing Population request")
                print(f"Got exception for Population request:\ngame={game_id}\n{str(err)}")
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
    