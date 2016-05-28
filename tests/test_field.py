import unittest

from amocrm.exceptions import *
from amocrm.values import Value
from amocrm.fields import Field

from .base_mocksettings import BaseMockSettingsTest


class TestField(BaseMockSettingsTest):
    def setUp(self):
        super().setUp()
        self.cls = Field

    def test_Field_needs_no_id(self):
        if self.cls == Field:
            return

        amovalue = self.amovalue_phone
        try:
            amofield = self.cls(values=amovalue)
        except MissingArgument:
            self.fail('id_ must be optional for Field children')

    def test_Field_gets_enum_if_present(self):
        self.mock_settings.DEFAULT_ENUM       = 1
        self.mock_settings.PHONE_DEFAULT_ENUM = 2
        self.mock_settings.EMAIL_DEFAULT_ENUM = 3
        self.mock_settings.URL_DEFAULT_ENUM   = 4
        self.mock_settings.NOTE_DEFAULT_ENUM  = 5

        value = 'some value'
        if self.cls == Field:
            id_   = 123 
            field = self.cls(id_=id_, values=value)
        else:
            id_   = self.cls.get_id() 
            field = self.cls(values=value)

        enum  = self.cls.get_enum()
        self.assertEqual(
            field.todict(), {
                'id': id_,
                'values': [{'value': value, 'enum': enum}],
            }
        )

    def test_Field_gets_no_enum_if_absent(self):
        self.mock_settings.DEFAULT_ENUM       = None
        self.mock_settings.PHONE_DEFAULT_ENUM = None
        self.mock_settings.EMAIL_DEFAULT_ENUM = None
        self.mock_settings.URL_DEFAULT_ENUM   = None
        self.mock_settings.NOTE_DEFAULT_ENUM  = None

        value = 'some value'
        if self.cls == Field:
            id_   = 123 
            field = self.cls(id_=id_, values=value)
        else:
            id_   = self.cls.get_id() 
            field = self.cls(values=value)
        enum  = self.cls.get_enum()

        self.assertEqual(
            field.todict(), {
                'id': id_,
                'values': [{'value': value}],
            }
        )



    def test_Field_accepts_one_Value(self):
        amovalue = self.amovalue_phone

        amofield = Field(
            id_=self.amofield_id,
            values=amovalue
            )

        # check if amovalue was wrapped in list
        self.assertEqual(
            amofield.values,
            [amovalue],
        )

        # full dict check
        d = amofield.todict()
        self.assertEqual(d, {
            "id": self.amofield_id,
            "values": [{
                "value": self.phone_value,
                "enum" : self.phone_enum,
            }]
        })

    def test_Field_accepts_multiple_Values(self):
        amovalue1 = self.amovalue_phone
        amovalue2 = self.amovalue_email
        amovalues = [amovalue1, amovalue2]

        amofield = Field(
            id_=self.amofield_id,
            values=amovalues
            )

        # check if amovalue was wrapped in list
        self.assertEqual(
            amofield.values,
            amovalues,
        )

        d = amofield.todict()
        self.assertEqual(d, {
            "id": self.amofield_id,
            "values": [
                {
                    "value": self.phone_value,
                    "enum" : self.phone_enum,
                },{
                    "value": self.email_value,
                    "enum" : self.email_enum,
                },

            ]
        })

    def test_Field_accepts_dict_of_values(self):
        d = {
            'value': 'some value',
            'whatever': 'something else',
        }
        field = Field(
            id_=self.amofield_id,
            values=d
        )

        self.assertEqual(
            field.todict(), {
                "id": self.amofield_id,
                "values": [d],
            }
        )

    def test_Field_accepts_string(self):
        value = 'some value'
        field = Field(
            id_=self.amofield_id,
            values=value
        )

        result = {
            "id": self.amofield_id,
            "values": [{'value': value }],
        }
        enum = Field.get_enum()
        if enum:
            result.update({'enum': enum})

        self.assertEqual(
            field.todict(),
            result,
        )



    def test_Field_raises_if_no_id(self):
        amovalue = self.amovalue_phone
        with self.assertRaises(MissingArgument):
            amofield = Field(values=amovalue) # should raise

    def test_Field_raises_if_no_values(self):
        amovalue = self.amovalue_phone
        with self.assertRaises(MissingArgument):
            amofield = Field(id_=self.amofield_id) # should raise

    def test_Field_is_json_serializable(self):
        amovalue = self.amovalue_phone
        amofield = Field(
            id_=self.amofield_id,
            values=amovalue,
            )
        try:
            s = str(amofield)
        except TypeError as e:
            self.fail('Field is not JSON serializable!')
