import unittest
from unittest import skip
from unittest.mock import patch

from amocrm.exceptions import MissingArgument
from amocrm.entities import Customer

from .base_mocksettings import BaseMockSettingsTest


class TestCustomer(BaseMockSettingsTest):

    def test_Customer_todict_returns_dict(self):
        amocustomer = Customer(
            name=self.name,
            status_id=123,
        )
        d = amocustomer.todict()
        self.assertIsNotNone(d)
        self.assertIsInstance(d, dict)

    def test_Customer_raises_on_empty_name(self):
        with self.assertRaises(MissingArgument):
            Customer(status_id=123)

    def test_Customer_builds_correct_dict(self):
        name = 'Vasya'
        status_id = 123

        amocustomer = Customer(
            name=name,
            status_id=status_id,
        )

        d = amocustomer.todict()
        self.assertEqual(d, {
            "request": {
                "customers": {
                    "add": [{
                        "name": name,
                    }]
                }
            }
        })

    def test_Customer_is_json_serializable(self):
        amocustomer = Customer(
            name=self.name,
            status_id=123
        )

        try:
            str(amocustomer)
        except TypeError as e:
            self.fail('Customer is not JSON serializable!')

    def test_Customer_accepts_single_tag(self):
        tag = 'some tag'

        amocustomer = Customer(
            name=self.name,
            fields=self.amofields,
            tags=tag,
        )

        self.assertEqual(
            amocustomer.tags,
            [tag],
        )

        d = amocustomer.todict()
        self.assertEqual(d, {
            "request": {
                "customers": {
                    "add": [{
                        "name": self.name,
                        "tags": tag,
                    }]
                }
            }
        })

    
    def test_Customer_accepts_multiple_tags_as_list(self):
        tags = ['master', 'amo']

        amocustomer = Customer(
            name=self.name,
            fields=self.amofields,
            tags=tags
        )

        self.assertEqual(
            amocustomer.tags,
            tags,
        )

        d = amocustomer.todict()
        self.assertEqual(d, {
            "request": {
                "customers": {
                    "add": [{
                        "name": self.name, 
                        "tags": ", ".join(tags),
                    }]
                }
            }
        })

    def test_Customer_accepts_multiple_tags_as_str(self):
        tags = 'master,amo'

        amocustomer = Customer(
            name=self.name,
            fields=self.amofields,
            tags=tags
        )

        expected_result = ['master', 'amo']

        self.assertEqual(
            amocustomer.tags,
            expected_result,
        )

        d = amocustomer.todict()
        self.assertEqual(d, {
            "request": {
                "customers": {
                    "add": [{
                        "name": self.name,
                        "tags": ', '.join(expected_result),
                    }]
                }
            }
        })
