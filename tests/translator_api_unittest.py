#
# Created on Mon Jan 04 2021
#
# Copyright Unai Garay Maestre, 2021
#

'''
Unit tests for summary API
'''

from fastapi.testclient import TestClient
from translator.api.server import app

import unittest
from unittest import mock
from easynmt import EasyNMT

class TranslatorAPITestCase(unittest.TestCase):
    '''
    Class for running unit tests on the Translator API
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Set up all tests
        '''
        super(TranslatorAPITestCase, cls).setUpClass()
    
    def setUp(self):
        '''
        Set up for each unit test
        '''
        self.client = TestClient(app)

    @mock.patch.object(EasyNMT, 'translate', autospec=True)
    def test_translate_endpoint(self, translator_mock):
        '''
        Testing translate endpoint
        '''
        # correct call
        data = {
            "sentences": [
                "Según el portal oficial de la organización, Microsoft tiene la intención de terminar formalmente sus operaciones contra Windows después del 14 de enero de 2020",
                "根据该组织的官方门户网站，微软公司打算在2020年1月14日之后正式终止对Windows "
            ],
            "target_lang": "en"
        }
        expected_results = [
            "According to the official website of the organization, Microsoft intends to formally terminate its operations against Windows after January 14, 2020",
            "According to the organization's official portal, Microsoft intends to formally terminate its operations against Windows after 14 January 2020 "
        ]
        translator_mock.return_value = expected_results
        response = self.client.post(
            '/translate',
            json=data
        )
        assert response.status_code == 200
        data = response.json()
        self.assertIn('translations', data)
        self.assertIsInstance(data['translations'], list)
        for translation in data['translations']:
            self.assertIsInstance(translation, str)
        self.assertEqual(data['translations'][0], expected_results[0])
        self.assertEqual(data['translations'][1], expected_results[1])

        # malformed requests
        response = self.client.post(
            '/translate',
            json={'sentences': "This is just one sentence"}
        )
        assert response.status_code == 422