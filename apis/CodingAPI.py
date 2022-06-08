# import standard libraries
import os
import traceback
from typing import Any, Dict, Optional
# import 3rd-party libraries
from flask import Flask, current_app
from flask_restful import Resource, Api, reqparse
from mysql.connector import Error as MySQLError
from mysql.connector.connection import MySQLConnection
# import locals
from apis.APIResult import APIResult, RESTType, ResultStatus
from apis import APIUtils
from config.config import settings
from opengamedata.coding.Code import Code
from opengamedata.coding.Coder import Coder
from opengamedata.interfaces.CodingInterface import CodingInterface
from opengamedata.schemas.IDMode import IDMode
from opengamedata.schemas.Request import Request, ExporterRange, ExporterTypes, ExporterLocations
from opengamedata.schemas.RequestResult import RequestResult

class CodingAPI:
    """API for logging and retrieving game states.
    Located at <server_addr>/player/<player_id>/game/<game_id>/state
    Valid requests are GET and POST.
    A GET request optionally takes 'count' and 'offset' as request parameters.
    A POST request should have a state variable as a request parameter.

    example usage:  GET fieldday-web.ad.education.wisc.edu/player/Bob/game/AQUALAB/state
                    with count=1, offset=0
    """
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(CodingAPI.CodeList,  '/coding/game/<game_id>/codewords')
        api.add_resource(CodingAPI.CoderList, '/coding/game/<game_id>/coders')
        api.add_resource(CodingAPI.Code,      '/coding/game/<game_id>/player/<player_id>/session/<session_id>/code/<code>/')

    class CoderList(Resource):
        def get(self, game_id:str):
            current_app.logger.info(f"Received request for {game_id} players.")
            ret_val = APIResult.Default(req_type=RESTType.POST)
            ret_val.RequestSucceeded(msg=f"SUCCESS: Got a (fake) list of codes for {game_id}", val=["Code1", "Code2", "Code3"])
            return ret_val.ToDict()

    class CodeList(Resource):
        def get(self, game_id:str):
            ret_val = APIResult.Default(req_type=RESTType.POST)
            ret_val.RequestSucceeded(msg=f"SUCCESS: Created a (fake) list of codes for {game_id}", val=["Code1", "Code2", "Code3"])
            return ret_val

    class Code(Resource):
        def post(self, game_id, player_id, session_id, code):
            current_app.logger.info(f"Received request for {game_id} players.")
            ret_val = APIResult.Default(req_type=RESTType.POST)

            # Step 1: get args
            parser = reqparse.RequestParser()
            parser.add_argument("indices", type=str, required=True, default="[]")
            parser.add_argument("coder",   type=str, required=True, default="default")
            parser.add_argument("notes",   type=str, required=False)
            args : Dict[str, Any] = parser.parse_args()

            _indices = APIUtils.parse_list(args.get('indices') or "[]")
            _events = []
            if _indices is not None:
                _events = [Code.EventID(sess_id=session_id, index=idx) for idx in _indices]
            try:
                _success = False
                os.chdir("var/www/opengamedata/")
                _interface : Optional[CodingInterface] = APIUtils.gen_coding_interface(game_id=game_id)
                if _interface is not None:
                    _success = _interface.CreateCode(code=code, coder_id=args.get('coder', "default"), events=_events, notes=args.get('notes', None))
                os.chdir("../../../../")
            except Exception as err:
                ret_val.ServerErrored(f"ERROR: {type(err).__name__} exception while processing Code request")
                current_app.logger.error(f"Got exception while processing Code request:\ngame={game_id}\n{str(err)}")
                current_app.logger.error(traceback.format_exc())
            else:
                if _success:
                    ret_val.RequestSucceeded(msg=f"SUCCESS: Added code with {len(_events)} events to database.", val=_success)
                else:
                    ret_val.RequestErrored(msg="FAIL: Unable to store code to database.")
                    ret_val.Value = _success
            return ret_val.ToDict()