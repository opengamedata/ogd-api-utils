# import libraries
import logging
import requests
import unittest
from multiprocessing import Process
from unittest import defaultTestLoader, TestResult, TestSuite
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
# import locals
from tests.cases.HelloAPI import *

class t_HelloAPI:
    @staticmethod
    def RunAll():
        cases = [
            t_Version,
            t_Hello,
            t_ParamHello
        ]
        suite : TestSuite = TestSuite(cases)
        print(f"Loaded {suite}")
        result = TestResult()
        suite.run(result)

if __name__ == '__main__':
    import os
    print(f"Running t_HelloAPI in {os.getcwd()}")
    t_HelloAPI.RunAll()