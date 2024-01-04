import logging
import os
import unittest

import saspy
from dotenv import load_dotenv
from saspy import SASsession

from src.sas_handler import SASHandler


class TestSASHandler(unittest.TestCase):
    _SAS: SASsession = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls._SAS = saspy.SASsession(url=os.getenv('VIYA_URI'),
                                    user=os.getenv('USER'), pw=os.getenv('PWD'),
                                    context='SAS Studio compute context')

    @classmethod
    def tearDownClass(cls):
        cls._SAS.endsas()

    def test_log_error(self):
        def create_sasHandler(level):
            handler = SASHandler(sas=self._SAS)
            handler.setLevel(level)
            return handler

        handler = create_sasHandler(logging.ERROR)
        logger: logging.Logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        logger.error("This is an error message")
        logger.debug("This is a debug message")

        self.assertTrue(
            "This is an error message" in self._SAS.lastlog()
        )
        self.assertTrue(
            "This is a debug message" not in self._SAS.lastlog()
        )

        print(self._SAS.saslog())
