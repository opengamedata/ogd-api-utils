# import standard libraries
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Type
# import local files
from ogd.core.schemas.Schema import Schema
from ogd.core.schemas.configs.data_sources.MySQLSourceSchema import MySQLSchema

class ServerConfigSchema(Schema):
    def __init__(self, name:str, all_elements:Dict[str, Any], logger:logging.Logger):
        self._state_dbs        : Dict[str, MySQLSchema]
        self._ogd_core         : Path
        self._google_client_id : str
        self._dbg_level        : int
        self._version          : int

        if "DB_CONFIG" in all_elements.keys():
            self._data_src = ServerConfigSchema._parseDataSources(all_elements["DB_CONFIG"], logger=logger)
        else:
            self._data_src = {}
            logger.warn(f"{name} config does not have a 'DB_CONFIG' element; defaulting to game_sources={self._data_src}", logging.WARN)
        if "OGD_CORE_PATH" in all_elements.keys():
            self._ogd_core = ServerConfigSchema._parseOGDPath(path=all_elements["OGD_CORE_PATH"], logger=logger)
        else:
            self._ogd_core = Path("./") / "opengamedata"
            logger.warn(f"{name} config does not have a 'OGD_CORE_PATH' element; defaulting to ogd_core_path={self._ogd_core}", logging.WARN)
        if "GOOGLE_CLIENT_ID" in all_elements.keys():
            self._google_client_id = ServerConfigSchema._parseGoogleID(google_id=all_elements["GOOGLE_CLIENT_ID"], logger=logger)
        else:
            self._google_client_id = "UNKNOWN ID"
            logger.warn(f"{name} config does not have a 'GOOGLE_CLIENT_ID' element; defaulting to google_client_id={self._google_client_id}", logging.WARN)
        if "DEBUG_LEVEL" in all_elements.keys():
            self._dbg_level = ServerConfigSchema._parseDebugLevel(all_elements["DEBUG_LEVEL"], logger=logger)
        else:
            self._dbg_level = logging.INFO
            logger.warn(f"{name} config does not have a 'DEBUG_LEVEL' element; defaulting to dbg_level={self._dbg_level}", logging.WARN)
        if "VER" in all_elements.keys():
            self._version = ServerConfigSchema._parseVersion(all_elements["VER"], logger=logger)
        else:
            self._version = -1
            logger.warn(f"{name} config does not have a 'VER' element; defaulting to version={self._version}", logging.WARN)

        _used = {"DB_CONFIG", "OGD_CORE_PATH", "GOOGLE_CLIENT_ID", "DEBUG_LEVEL", "VER"}
        _leftovers = { key : val for key,val in all_elements.items() if key not in _used }
        super().__init__(name=name, other_elements=_leftovers)

    @property
    def StateDatabases(self) -> Dict[str, MySQLSchema]:
        return self._state_dbs

    @property
    def OGDCore(self) -> Path:
        return self._ogd_core

    @property
    def GoogleClientID(self) -> str:
        return self._google_client_id

    @property
    def DebugLevel(self) -> int:
        return self._dbg_level

    @property
    def Version(self) -> int:
        return self._version

    @property
    def AsMarkdown(self) -> str:
        ret_val : str

        ret_val = f"{self.Name}"
        return ret_val

    @staticmethod
    def _parseDataSources(sources, logger:logging.Logger) -> Dict[str, MySQLSchema]:
        ret_val : Dict[str, MySQLSchema]
        if isinstance(sources, dict):
            ret_val = {}
            for key,val in sources.items():
                ret_val[key] = MySQLSchema(name=key, all_elements=val)
        else:
            ret_val = {}
            logger.warn(f"Config data sources was unexpected type {type(sources)}, defaulting to empty dict: {ret_val}.", logging.WARN)
        return ret_val

    @staticmethod
    def _parseOGDPath(path, logger:logging.Logger) -> Path:
        ret_val : Path
        if isinstance(path, str):
            ret_val = Path(path)
        else:
            ret_val = Path("./") / "opengamedata"
            logger.warn(f"Data Source DB type was unexpected type {type(path)}, defaulting to path={ret_val}.", logging.WARN)
        return ret_val

    @staticmethod
    def _parseGoogleID(google_id, logger:logging.Logger) -> str:
        ret_val : str
        if isinstance(google_id, str):
            ret_val = google_id
        else:
            ret_val = str(google_id)
            logger.warn(f"Google Client ID type was unexpected type {type(google_id)}, defaulting to google_client_id=str({ret_val}).", logging.WARN)
        return ret_val

    @staticmethod
    def _parseDebugLevel(level, logger:logging.Logger) -> int:
        ret_val : int
        if isinstance(level, str):
            match level.upper():
                case "ERROR":
                    ret_val = logging.ERROR
                case "WARNING" | "WARN":
                    ret_val = logging.WARN
                case "INFO":
                    ret_val = logging.INFO
                case "DEBUG":
                    ret_val = logging.DEBUG
                case _:
                    ret_val = logging.INFO
                    logger.warn(f"Config debug level had unexpected value {level}, defaulting to logging.INFO.", logging.WARN)
        else:
            ret_val = logging.INFO
            logger.warn(f"Config debug level was unexpected type {type(level)}, defaulting to logging.INFO.", logging.WARN)
        return ret_val

    @staticmethod
    def _parseVersion(version, logger:logging.Logger) -> int:
        ret_val : int
        if isinstance(version, int):
            ret_val = version
        elif isinstance(version, str):
            ret_val = int(version)
        else:
            ret_val = int(str(version))
            logger.warn(f"Config version was unexpected type {type(version)}, defaulting to int(str(version))={ret_val}.", logging.WARN)
        return ret_val
