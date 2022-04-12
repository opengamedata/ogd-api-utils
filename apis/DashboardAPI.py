"""Module for the Dashboard API code
"""
# import libraries
import os
import traceback
from flask import Flask, current_app
from flask_restful import Resource, Api
from typing import List
# import locals
from apis import APIUtils
from config.config import settings
from apis.APIResult import APIResult, RESTType, ResultStatus
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
