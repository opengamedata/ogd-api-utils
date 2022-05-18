# import libraries
import json
from flask import current_app
from typing import Any, List, Union
# import locals
from config.config import settings
import opengamedata.utils
from opengamedata.interfaces.MySQLInterface import MySQLInterface
from opengamedata.interfaces.BigQueryInterface import BigQueryInterface

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
            current_app.logger.info(f"Using MySQLInterface for {game_id}")
        elif src_map['interface'] == "BigQuery":
            ret_val = BigQueryInterface(game_id=game_id, settings=settings)
            current_app.logger.info(f"Using BigQueryInterface for {game_id}")
        else:
            ret_val = MySQLInterface(game_id, settings=settings)
            current_app.logger.warning(f"Could not find a valid interface for {game_id}, defaulting to MySQL!")
    return ret_val
