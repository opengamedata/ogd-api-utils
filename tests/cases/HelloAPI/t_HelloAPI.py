# Set up logging
import logging
from ogd.core.utils.Logger import Logger
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)

# Set up path
import os, sys
from pprint import pprint
from pathlib import Path

sys.path.insert(0, str(Path(os.getcwd()) / "src"))

import unittest
loader = unittest.TestLoader()
print(f"Running discovery in {os.getcwd()}")
tests = loader.discover('./tests/cases/HelloAPI/resources', pattern="t_Hello*.py", top_level_dir="./")
print(f"Updated path:")
pprint(sys.path[:5])
print(f"Tests are:")
for ts in tests._tests:
    if isinstance(ts, unittest.TestSuite):
        pprint([t._tests if isinstance(t, unittest.TestSuite) else t for t in ts])

testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
print("Done with t_HelloAPI")