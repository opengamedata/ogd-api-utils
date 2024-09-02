# Set up logging
import logging
from ogd.core.utils.Logger import Logger
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)

# Set up path
from pprint import pprint
# Set up path
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(os.getcwd()) / "src"))
print(f"Updated path:")
pprint(sys.path[:5])
import unittest

loader = unittest.TestLoader()
print("Preparing discovery")
tests = loader.discover('./tests/cases/HelloAPI', pattern="t_Hello*.py", top_level_dir="./")
print("Finished discovery")
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)