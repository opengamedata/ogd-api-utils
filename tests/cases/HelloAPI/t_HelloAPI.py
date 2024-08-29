# import libraries
import logging
import requests
import unittest
from multiprocessing import Process
from unittest import defaultTestLoader, TestResult
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
# import locals
import tests.cases.HelloAPI
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)

class t_HelloAPI:
    @staticmethod
    def RunAll():
        suite = defaultTestLoader.loadTestsFromModule(tests.cases.HelloAPI)
        result = TestResult()
        suite.run(result)
