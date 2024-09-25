"""
ServerConfigSchema

Contains a Schema class for managing config data for server configurations.
"""

# import standard libraries
import logging
from typing import Any, Dict

# import 3rd-party libraries

# import OGD libraries
from ogd.common.schemas.Schema import Schema
from ogd.common.utils.SemanticVersion import SemanticVersion

# import local files

class ServerConfigSchema(Schema):
    @staticmethod
    def DEFAULT():
        return ServerConfigSchema(
            name="DefaultServerConfig",
            debug_level=logging.DEBUG,
            version=SemanticVersion.FromString("0.0.0-Testing"),
            other_elements={}
        )

    def __init__(self, name:str, debug_level:int, version:SemanticVersion, other_elements:Dict[str, Any]):
        self._dbg_level : int             = debug_level
        self._version   : SemanticVersion = version
        super().__init__(name=name, other_elements=other_elements)

    @staticmethod
    def FromDict(name:str, all_elements:Dict[str, Any], logger:logging.Logger):
        _dbg_level : int
        _version   : SemanticVersion

        if "API_VERSION" in all_elements.keys():
            _version = ServerConfigSchema._parseVersion(all_elements["API_VERSION"], logger=logger)
        else:
            _version = SemanticVersion.FromString("UNKNOWN VERSION")
            logger.warning(f"{name} config does not have an 'API_VERSION' element; defaulting to version={_version}", logging.WARN)
        if "DEBUG_LEVEL" in all_elements.keys():
            _dbg_level = ServerConfigSchema._parseDebugLevel(all_elements["DEBUG_LEVEL"], logger=logger)
        else:
            _dbg_level = logging.INFO
            logger.warning(f"{name} config does not have a 'DEBUG_LEVEL' element; defaulting to dbg_level={_dbg_level}", logging.WARN)

        _used = {"DEBUG_LEVEL", "API_VERSION"}
        _leftovers = { key : val for key,val in all_elements.items() if key not in _used }
        return ServerConfigSchema(name=name, debug_level=_dbg_level, version=_version, other_elements=_leftovers)


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
                    logger.warning(f"Config debug level had unexpected value {level}, defaulting to logging.INFO.", logging.WARN)
        else:
            ret_val = logging.INFO
            logger.warning(f"Config debug level was unexpected type {type(level)}, defaulting to logging.INFO.", logging.WARN)
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
            logger.warning(f"Config version was unexpected type {type(version)}, defaulting to SemanticVersion(str(version))={ret_val}.", logging.WARN)
        return ret_val
