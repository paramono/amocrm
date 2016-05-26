import requests
from requests.exceptions import RequestException

import unittest
from unittest import skip
from unittest.mock import patch, MagicMock

import amocrm.conf
from amocrm.manager import (
    Manager,
    AuthFailed,
    WrongStatusCode,
    NoCookieError,
    XmlReturnedFalse,
)

from .base_settings import BaseTestWithSettings
from .base_field_value import BaseTest


class ManagerTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        # SIC! XML below is copied from AmoCRM response as-is,
        # (although with dummy values in id, name and subdomain)
        cls.auth_xml = """
        <root>
                <auth>%s</auth>
                        <accounts>
                        <account>
                                <id>1234567</id>
                                <name>name</name>
                                <subdomain>subdomain</subdomain>
                        </account>
                </accounts>
                </root>
        """

    def get_response_xml(self, auth_string='true'):
        return self.auth_xml % auth_string

    def setUp(self):
        super().setUp()
        self.am = Manager()
        assert amocrm.conf.settings is self.mock_settings

    def tearDown(self):
        del self.am
        super().tearDown()

    @patch('requests.post')
    def test_auth_raises_on_wrong_status_code(self, mock_post):
        mock_post.return_value.status_code = 401
        with self.assertRaises(WrongStatusCode):
            r = self.am.auth()
            self.assertEqual(r.status_code, 401)
        assert mock_post.called

    @patch('requests.post')
    def test_auth_raises_on_empty_cookie(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.cookies = None
        with self.assertRaises(NoCookieError):
            r = self.am.auth()
            self.assertEqual(r.status_code, 404)
        assert mock_post.called

    @patch('requests.post')
    def test_auth_raises_on_false_in_xml(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.cookies = 'some cookie'
        mock_post.return_value.text = self.get_response_xml(auth_string='false')

        with self.assertRaises(XmlReturnedFalse):
            r = self.am.auth()
            self.assertEqual(self.am.cookies, r.cookies)
        assert mock_post.called

    @patch('requests.post')
    def test_auth_success(self, mock_post):
        # mock_post = Mock
        assert amocrm.conf.settings is self.mock_settings
        assert requests.post is mock_post
        mock_post.return_value.text = self.get_response_xml(auth_string='true')
        mock_post.return_value.status_code = 200
        mock_post.return_value.cookies = 'some cookie'

        r = self.am.auth()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.am.cookies, r.cookies)
        self.assertEqual(
            r.text,
            self.get_response_xml(auth_string='true')
        )
        assert mock_post.called
