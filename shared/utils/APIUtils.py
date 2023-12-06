# import libraries
from flask import current_app
from typing import Any, Dict, List, Optional
# import locals
from config.config import settings as server_settings
from config.coreconfig import settings as core_settings
# from ogd.core.interfaces.CodingInterface import CodingInterface
from ogd.core.interfaces.DataInterface import DataInterface
from ogd.core.interfaces.MySQLInterface import MySQLInterface
from ogd.core.interfaces.BigQueryInterface import BigQueryInterface
from ogd.core.interfaces.BigQueryCodingInterface import BigQueryCodingInterface
from ogd.core.schemas.configs.ConfigSchema import ConfigSchema
from ogd.core.schemas.configs.GameSourceSchema import GameSourceSchema

def parse_list(list_str:str) -> Optional[List[Any]]:
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

def gen_interface(game_id) -> Optional[DataInterface]:
    """Utility to set up an Interface object for use by the API, given a game_id.

    :param game_id: _description_
    :type game_id: _type_
    :return: _description_
    :rtype: _type_
    """
    ret_val = None
    
    _core_config = ConfigSchema(name="Core Config", all_elements=core_settings)
    _game_source : GameSourceSchema = _core_config.GameSourceMap.get(game_id, GameSourceSchema.EmptySchema())

    if _game_source.Source is not None:
        # set up interface and request
        if _game_source.Source.Type == "MySQL":
            ret_val = MySQLInterface(game_id, config=_game_source, fail_fast=False)
            current_app.logger.info(f"Using MySQLInterface for {game_id}")
        elif _game_source.Source.Type == "BigQuery":
            ret_val = BigQueryInterface(game_id=game_id, config=_game_source, fail_fast=False)
            current_app.logger.info(f"Using BigQueryInterface for {game_id}")
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
