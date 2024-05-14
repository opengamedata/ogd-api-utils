"""
APIUtils

Contains general utility functions for common  tasks when setting up our flask/flask-restful API functions.
In particular, has functions to assist in parsing certain kinds of data, and for generating OGD-core objects.
"""

# import standard libraries
import json
import os
from typing import Any, List, Optional

# import 3rd-party libraries
from flask import current_app

# import OGD libraries
from ogd.core.interfaces.DataInterface import DataInterface
from ogd.core.interfaces.MySQLInterface import MySQLInterface
from ogd.core.interfaces.BigQueryInterface import BigQueryInterface
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.schemas.configs.GameSourceSchema import GameSourceSchema

# import local files

def parse_list(list_str:str) -> Optional[List[Any]]:
    """Simple utility to parse a string containing a bracketed list into a Python list.
    Returns None if the list was empty

    :param list_str: _description_
    :type list_str: str
    :return: A list parsed from the input string, or None if the string list was invalid or empty.
    :rtype: Union[List[Any], None]
    """
    ret_val : Optional[List[Any]] = None
    try:
        ret_val = json.loads(list_str)
    except json.decoder.JSONDecodeError as e:
        current_app.logger.warn(f"Could not parse '{list_str}' as a list, format was not valid!\nGot Error {e}")
    else:
        if ret_val is not None and len(ret_val) == 0:
            # If we had empty list, just treat as null.
            ret_val = None
    return ret_val

def gen_interface(game_id, core_config:ConfigSchema) -> Optional[DataInterface]:
    """Utility to set up an Interface object for use by the API, given a game_id.

    :param game_id: _description_
    :type game_id: _type_
    :return: _description_
    :rtype: _type_
    """
    ret_val = None
    
    _game_source : GameSourceSchema = core_config.GameSourceMap.get(game_id, GameSourceSchema.EmptySchema())

    if _game_source.Source is not None:
        # set up interface and request
        if _game_source.Source.Type.upper() == "MYSQL":
            ret_val = MySQLInterface(game_id, config=_game_source, fail_fast=False)
            current_app.logger.info(f"Using MySQLInterface for {game_id}")
        elif _game_source.Source.Type.upper() == "BIGQUERY":
            current_app.logger.info(f"Generating BigQueryInterface for {game_id}, from directory {os.getcwd()}...")
            ret_val = BigQueryInterface(game_id=game_id, config=_game_source, fail_fast=False)
            current_app.logger.info("Done")
        else:
            ret_val = MySQLInterface(game_id, config=_game_source, fail_fast=False)
            current_app.logger.warning(f"Could not find a valid interface for {game_id}, defaulting to MySQL!")
    return ret_val

# def gen_coding_interface(game_id) -> Optional[CodingInterface]:
#     """Utility to set up an Interface object for use by the API, given a game_id.

#     :param game_id: _description_
#     :type game_id: _type_
#     :return: _description_
#     :rtype: _type_
#     """
#     ret_val = None

#     _core_config = ConfigSchema(name="Core Config", all_elements=core_settings)
#     _game_source : GameSourceSchema = _core_config.GameSourceMap.get(game_id, GameSourceSchema.EmptySchema())

#     if _game_source.Source is not None:
#         # set up interface and request
#         if _game_source.Source.Type == "BigQuery":
#             ret_val = BigQueryCodingInterface(game_id=game_id, config=_core_config)
#             current_app.logger.info(f"Using BigQueryCodingInterface for {game_id}")
#         else:
#             ret_val = BigQueryCodingInterface(game_id=game_id, config=_core_config)
#             current_app.logger.warning(f"Could not find a valid interface for {game_id}, defaulting to BigQuery!")
#     return ret_val
