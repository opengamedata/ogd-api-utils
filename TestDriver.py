from tests.cases.utils.t_APIResponse import t_APIResponse
from tests.cases.utils.t_APIUtils import t_APIUtils
from tests.cases.schemas.t_ServerConfigSchema import t_ServerConfigSchema
from tests.cases.utils.t_HelloAPI import t_HelloAPI

from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="APIUtilsTestConfig", all_elements=settings, logger=None)


if _config.EnabledTests.get('CONFIG'):
    test_Utils = t_ServerConfigSchema()
    print("***\nRunning test_ServerConfigSchema:\n")
    test_Utils.RunAll()
    print("Done\n***")
if _config.EnabledTests.get('RESPONSE'):
    test_APIResponse = t_APIResponse()
    print("***\nRunning test_APIResponse:")
    test_APIResponse.RunAll()
    print("Done\n***")
if _config.EnabledTests.get('UTILS'):
    test_Utils = t_APIUtils()
    print("***\nRunning test_APIUtils:\n")
    test_Utils.RunAll()
    print("Done\n***")
if _config.EnabledTests.get('HELLO'):
    test_Hello = t_HelloAPI()
    print("***\nRunning test_Hello:")
    test_Hello.RunAll()
    print("Done\n***")