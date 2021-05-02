#
# Created on Mon Jan 04 2021
#
# Copyright Unai Garay Maestre, 2021
#

'''
Unit tests for summary API
'''

from fastapi.testclient import TestClient
from summariser.api.server import app

import unittest

class SummariserAPITestCase(unittest.TestCase):
    '''
    Class for running unit tests on the Summariser API
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Set up all tests
        '''
        super(SummariserAPITestCase, cls).setUpClass()
    
    def setUp(self):
        '''
        Set up for each unit test
        '''
        self.client = TestClient(app)

    def test_summarise_endpoint(self):
        '''
        Testing summarise endpoint
        '''
        # correct call
        data = {
            "sentences": [
                "Microsoft Corporation intends to officially end free support for the Windows 7 operating system",
                "根据该组织的官方门户网站，微软公司打算在2020年1月14日之后正式终止对Windows "
            ]
        }
        response = self.client.post(
            '/summarise',
            json=data
        )
        assert response.status_code == 200
        data = response.json()
        self.assertIn('summaries', data)
        self.assertIsInstance(data['summaries'], list)
        for summary in data['summaries']:
            self.assertIsInstance(summary, str)

        # malformed requests
        response = self.client.post(
            '/summarise',
            json={'sentences': "This is just one sentence"}
        )
        assert response.status_code == 422