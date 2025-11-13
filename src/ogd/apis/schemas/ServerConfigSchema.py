"""
ServerConfig

Contains a Config class for managing config data for server configurations.
"""

# import standard libraries
import logging
from typing import Dict, Final, Optional

# import 3rd-party libraries

# import OGD libraries
from ogd.common.configs.Config import Config
from ogd.common.models.SemanticVersion import SemanticVersion
from ogd.common.utils.typing import Map

# import local files

class ServerConfig(Config):
    _DEFAULT_DEBUG_LEVEL : Final[int] = logging.INFO
    _DEFAULT_VERSION     : Final[str] = "UNKNOWN VERSION"

    # *** BUILT-INS & PROPERTIES ***

    def __init__(self, name:str,
                 debug_level:Optional[int], version:Optional[SemanticVersion],
                 other_elements:Optional[Map]=None):

        unparsed_elements : Map = other_elements or {}

        self._dbg_level : int
        self._version   : SemanticVersion

        if "API_VERSION" in unparsed_elements.keys():
            _version = ServerConfig._parseVersion(all_elements["API_VERSION"], logger=logger)
        else:
            _version = SemanticVersion.FromString("UNKNOWN VERSION")
            logger.warning(f"{name} config does not have an 'API_VERSION' element; defaulting to version={_version}", logging.WARN)
        if "DEBUG_LEVEL" in all_elements.keys():
            _dbg_level = ServerConfig._parseDebugLevel(all_elements["DEBUG_LEVEL"], logger=logger)
        else:
            _dbg_level = logging.INFO
            logger.warning(f"{name} config does not have a 'DEBUG_LEVEL' element; defaulting to dbg_level={_dbg_level}", logging.WARN)

        super().__init__(name=name, other_elements=other_elements)


    @property
    def DebugLevel(self) -> int:
        return self._dbg_level

    @property
    def Version(self) -> SemanticVersion:
        return self._version

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***

    @property
    def AsMarkdown(self) -> str:
        ret_val : str

        ret_val = f"{self.Name}"
        return ret_val

    @classmethod
    def Default(cls):
        return ServerConfig(
            name="DefaultServerConfig",
            debug_level=logging.DEBUG,
            version=SemanticVersion.FromString("0.0.0-Testing"),
            other_elements={}
        )

    @classmethod
    def _fomDict(cls, name:str, unparsed_elements:Map,
                  key_overrides:Optional[Dict[str, str]]=None,
                  default_override:Optional[Self]=None):
        _dbg_level : int
        _version   : SemanticVersion

        _used = {"DEBUG_LEVEL", "API_VERSION"}
        _leftovers = { key : val for key,val in all_elements.items() if key not in _used }
        return ServerConfig(name=name, debug_level=_dbg_level, version=_version, other_elements=_leftovers)

    @staticmethod
    def _parseDebugLevel(unparsed_elements:Map, schema_name:Optional[str]=None, logger:logging.Logger=flask) -> int:
        ret_val : int
        raw_level : str = ServerConfig.ParseElement(
            unparsed_elements=unparsed_elements,
            valid_keys=["DEBUG_LEVEL"],
            to_type=str,
            default_value=ServerConfig._DEFAULT_DEBUG_LEVEL,
            remove_target=True,
            schema_name=schema_name
        )
        match raw_level.upper():
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
                logger.warning(f"Config debug level had unexpected value {raw_level}, defaulting to logging.INFO.", logging.WARN)
        else:
            ret_val = logging.INFO
            logger.warning(f"Config debug level was unexpected type {type(raw_level)}, defaulting to logging.INFO.", logging.WARN)
        return ret_val

    @staticmethod
    def _parseVersion(unparsed_elements:Map, schema_name:Optional[str]=None) -> SemanticVersion:
        ret_val : SemanticVersion
        if isinstance(version, int):
            ret_val = SemanticVersion(major=version)
        elif isinstance(version, str):
            ret_val = SemanticVersion.FromString(semver=version)
        else:
            ret_val = SemanticVersion.FromString(str(version))
            logger.warning(f"Config version was unexpected type {type(version)}, defaulting to SemanticVersion(str(version))={ret_val}.", logging.WARN)
        return ret_val
