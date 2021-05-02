#
# Created on Mon Jan 04 2021
#
# Copyright Unai Garay Maestre, 2021
#

'''
Unit tests for summary models
'''

import unittest
import logging
import config

from summariser.core.summariser import Summariser

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(levelname)s:%(message)s')

def _log_test_title(title):
    line = '=' * len(title)
    logging.info('\n\n%s\n%s\n%s' % (line, title, line))


class SummariserUnitTest(unittest.TestCase):
    '''
    Class for running unit tests for summarising model
    '''

    def test_summariser(self):
        '''
        Test Summariser
        '''
        _log_test_title('Test Summariser')

        summariser = Summariser()
        test_paragraphs = [
            "Microsoft Corporation intends to officially end free support for the Windows 7 operating system after January 14, 2020, according to the official portal of the organization. From that day, users of this system will not be able to receive security updates, which could make their computers vulnerable to cyber attacks.",
            "орпорация Microsoft намерена официально прекратить бесплатную поддержку операционной системы Windows 7 после 14 января 2020 года, сообщается на официальном портале организации . С указанного дня пользователи этой системы не смогут получать обновления безопасности, из-за чего их компьютеры могут стать уязвимыми к кибератакам.",
            "根据该组织的官方门户网站，微软公司打算在2020年1月14日之后正式终止对Windows 7操作系统的免费支持。从那时起，该系统的用户将无法接收安全更新，这可能会使他们的计算机容易受到网络攻击。"
        ]
        summaries = summariser.summarise(test_paragraphs)

        summaries_expected = [
            "Microsoft to end Windows 7 free support after January 14, 2020",
            "Microsoft намерена прекратить бесплатную поддержку Windows 7 после 14 января 2020 года",
            "微软终止对Windows 7操作系统的免费支持"
        ]

        self.assertEqual(3, len(summaries))
        self.assertEqual(summaries[0], summaries_expected[0])
        self.assertEqual(summaries[1], summaries_expected[1])
        self.assertEqual(summaries[2], summaries_expected[2])