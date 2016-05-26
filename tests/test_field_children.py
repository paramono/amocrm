import unittest

from amocrm.exceptions import *
from amocrm.models.field import (
    Field,
    PhoneField,
    EmailField,
    NoteField,
    UrlField,
)

from .base_field_value import BaseTest
from .test_field import TestField


class TestPhoneField(TestField):

    def setUp(self):
        super().setUp()
        self.cls = PhoneField


class TestEmailField(TestField):

    def setUp(self):
        super().setUp()
        self.cls = EmailField


class TestUrlField(TestField):

    def setUp(self):
        super().setUp()
        self.cls = UrlField


class TestNoteField(TestField):

    def setUp(self):
        super().setUp()
        self.cls = NoteField
