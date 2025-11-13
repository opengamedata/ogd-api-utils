# Standard imports
from unittest import defaultTestLoader, TestLoader, TestSuite, runner

# Set up path
import os, sys
from pprint import pprint
from pathlib import Path

sys.path.insert(0, str(Path(os.getcwd()) / "src"))
# Set up logging
import logging
from ogd.common.utils.Logger import Logger
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)

from ogd.common.configs.TestConfig import TestConfig
from config.t_config import settings

_config = TestConfig.FromDict(name="APIUtilsTestConfig", all_elements=settings)

# loader = TestLoader()
suite = TestSuite()
if _config.EnabledTests.get('CONFIG'):
    print("***\nAdding t_ServerConfigSchema:")
    suite.addTest(defaultTestLoader.discover('./tests/cases/schemas/', pattern="t_ServerConfigSchema.py", top_level_dir="./"))
    print("Done\n***")
if _config.EnabledTests.get('RESPONSE'):
    print("***\nAdding t_APIResponse:")
    suite.addTest(defaultTestLoader.discover('./tests/cases/utils/', pattern="t_APIResponse.py", top_level_dir="./"))
    print("Done\n***")
if _config.EnabledTests.get('UTILS'):
    print("***\nAdding t_APIUtils:")
    suite.addTest(defaultTestLoader.discover('./tests/cases/utils/', pattern="t_APIUtils.py", top_level_dir="./"))
    print("Done\n***")
if _config.EnabledTests.get('HELLO'):
    print("***\nAdding test_Hello:")
    suite.addTest(defaultTestLoader.discover('./tests/cases/apis/HelloAPI', pattern="t_*.py", top_level_dir="./"))
    print("Done\n***")

print(f"Tests are:")
for ts in suite._tests:
    if isinstance(ts, TestSuite):
        pprint([t._tests if isinstance(t, TestSuite) else t for t in ts])

testRunner = runner.TextTestRunner()
testRunner.run(suite)