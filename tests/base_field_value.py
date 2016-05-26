import unittest
from unittest.mock import patch

import amocrm.conf
# from settings import AmoSettings, amo_settings
from amocrm.models.field import (
    Field,
    PhoneField,
    EmailField,
    UrlField,
    NoteField,
)
from amocrm.models.value import Value


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.settings_patcher = patch('amocrm.conf.settings')
        self.mock_settings = self.settings_patcher.start()

        assert amocrm.conf.settings is self.mock_settings

        self.mock_settings.PHONE_ID = 123
        self.mock_settings.EMAIL_ID = 124
        self.mock_settings.URL_ID   = 125
        self.mock_settings.NOTE_ID  = 126


        self.mock_settings.USER_DOMAIN = 'https://example.amocrm.ru'

        self.phone_value = '555 55 55'
        self.phone_enum  = 'HOME'

        self.email_value = 'vasya@pupkin.com'
        self.email_enum  = 'EMAIL'

        self.mock_settings.DEFAULT_ENUM = None
        self.mock_settings.PHONE_DEFAULT_ENUM = self.phone_enum
        self.mock_settings.EMAIL_DEFAULT_ENUM = self.email_enum
        self.mock_settings.URL_DEFAULT_ENUM   = None
        self.mock_settings.NOTE_DEFAULT_ENUM  = None

        self.url_value  = 'example.org'
        self.note_value = 'note to self'

        self.amofield_id = 10

        # values
        self.amovalue_phone = Value(
            value=self.phone_value,
            enum=self.phone_enum,
            )
        self.amovalue_email = Value(
            value=self.email_value,
            enum=self.email_enum,
            )
        self.amovalue_url = Value(
            value=self.url_value,
            )
        self.amovalue_note = Value(
            value=self.note_value,
            )

        # fields
        self.amofield_phone = PhoneField(
            values=self.amovalue_phone,
            )
        self.amofield_email = EmailField(
            values=self.amovalue_email,
            )
        self.amofield_url = UrlField(
            values=self.amovalue_url,
            )
        self.amofield_note = NoteField(
            values=self.amovalue_note,
            )

        self.amofields = [
            self.amofield_phone,
            self.amofield_email,
            self.amofield_url,
            self.amofield_note,
        ]

        # contact
        self.name = 'Vasya'

    def tearDown(self):
        # pass
        self.settings_patcher.stop()


    # @classmethod
    # # @patch('settings.amo_settings')
    # def setUpClass(cls):

