import unittest
from unittest.mock import patch

import amocrm.conf


class BaseCopySettings(unittest.TestCase):

    def setUp(self):
        self.conf = amocrm.conf.AmoSettings()
        self.domain = 'https://example.amocrm.ru'
        self.user_login = 'vasya'
        self.user_hash  = 'hash'

    def tearDown(self):
        del self.conf

    def check_conf_is_empty(self):
        self.assertEqual(
            self.conf.__dict__,
            {'_dict': {}},
        )

    def set_domain(self):
        self.conf.USER_DOMAIN = self.domain

    def set_auth_data(self):
        self.conf.USER_LOGIN = self.user_login
        self.conf.USER_HASH  = self.user_hash

