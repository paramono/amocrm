import unittest

from amocrm.exceptions import *
from amocrm.values import Value

from .base_mocksettings import BaseMockSettingsTest


class TestValue(BaseMockSettingsTest):

    def test_Value_builds_correct_dict(self):
        amovalue = self.amovalue_phone
        d = amovalue.todict()
        self.assertEqual(d, {
            "value": self.phone_value,
            "enum" : self.phone_enum,
            }
        )

    def test_Value_is_json_serializable(self):
        amovalue = self.amovalue_phone

        try:
            s = str(amovalue)
        except TypeError as e:
            self.fail('Value is not JSON serializable!')

    def test_Value_raises_if_no_value(self):
        with self.assertRaises(MissingValue):
            amovalue = Value()
