#
# Created on Mon Jan 04 2021
#
# Copyright Unai Garay Maestre, 2021
#
'''
Unit tests for Summarisation
'''

import unittest
import os
import logging
import sys

from tests.translator_api_unittest import TranslatorAPITestCase

assert TranslatorAPITestCase

sys.path.append(os.getcwd())

if __name__ == "__main__":
    logging.basicConfig(level=config.LOGGING_LEVEL,
                        format='%(levelname)s:%(message)s')
    unittest.main()