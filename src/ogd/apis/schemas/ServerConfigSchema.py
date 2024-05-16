"""
ServerConfigSchema

Contains a Schema class for managing config data for server configurations.
"""

# import standard libraries
import logging
from typing import Any, Dict

# import 3rd-party libraries

# import OGD libraries
from ogd.core.schemas.Schema import Schema
from ogd.core.utils.SemanticVersion import SemanticVersion

# import local files

class ServerConfigSchema(Schema):
    def __init__(self, name:str, all_elements:Dict[str, Any], logger:logging.Logger):
        self._dbg_level : int
        self._version   : SemanticVersion

        if "DEBUG_LEVEL" in all_elements.keys():
            self._dbg_level = ServerConfigSchema._parseDebugLevel(all_elements["DEBUG_LEVEL"], logger=logger)
        else:
            self._dbg_level = logging.INFO
            logger.warn(f"{name} config does not have a 'DEBUG_LEVEL' element; defaulting to dbg_level={self._dbg_level}", logging.WARN)
        if "VER" in all_elements.keys():
            self._version = ServerConfigSchema._parseVersion(all_elements["VER"], logger=logger)
        else:
            self._version = SemanticVersion.FromString("UNKNOWN VERSION")
            logger.warn(f"{name} config does not have a 'VER' element; defaulting to version={self._version}", logging.WARN)

        _used = {"DB_CONFIG", "OGD_CORE_PATH", "GOOGLE_CLIENT_ID", "DEBUG_LEVEL", "VER"}
        _leftovers = { key : val for key,val in all_elements.items() if key not in _used }
        super().__init__(name=name, other_elements=_leftovers)

    @property
    def DebugLevel(self) -> int:
        return self._dbg_level

    @property
    def Version(self) -> SemanticVersion:
        return self._version

    @property
    def AsMarkdown(self) -> str:
        ret_val : str

        ret_val = f"{self.Name}"
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
    def _parseVersion(version, logger:logging.Logger) -> SemanticVersion:
        ret_val : SemanticVersion
        if isinstance(version, int):
            ret_val = SemanticVersion(major=version)
        elif isinstance(version, str):
            ret_val = SemanticVersion.FromString(semver=version)
        else:
            ret_val = SemanticVersion.FromString(str(version))
            logger.warn(f"Config version was unexpected type {type(version)}, defaulting to SemanticVersion(str(version))={ret_val}.", logging.WARN)
        return ret_val
