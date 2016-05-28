import unittest
from unittest import skip
from unittest.mock import patch

from amocrm.exceptions import *
from amocrm.entities import Lead

from .base_mocksettings import BaseMockSettingsTest


class TestLead(BaseMockSettingsTest):

    def test_Lead_todict_returns_dict(self):
        amolead = Lead(
            name=self.name,
            status_id=123,
        )
        d = amolead.todict()
        self.assertIsNotNone(d)
        self.assertIsInstance(d, dict)

    def test_Lead_raises_on_empty_name(self):
        with self.assertRaises(MissingArgument):
            amolead = Lead(
                status_id=123,
            )

    def test_Lead_raises_on_empty_status_id(self):
        with self.assertRaises(MissingArgument):
            amolead = Lead(
                name=self.name,
            )

    def test_Lead_builds_correct_dict(self):
        name = 'Vasya'
        status_id = 123

        amolead = Lead(
            name=name,
            status_id=status_id,
        )

        d = amolead.todict()
        self.assertEqual(d, {
            "request": {
                "leads": {
                    "add": [{
                        "name": name,
                        "status_id": status_id,
                        # "status_id":"9211617", # главная воронка
                        # "date_create":1298904164,
                        # "last_modified":1298904164,
                        # "price":300000,
                        # "responsible_user_id":215302,
                        # "tags": "Заявка,beta",
                        # "custom_fields":[{
                        #     "id":461512,
                        #     "values":[{
                        #         "value": 9776621,
                        #         "enum": "HOME"
                        #     }]
                        # }]
                    }]
                }
            }
        })

    def test_Lead_is_json_serializable(self):
        amolead = Lead(
            name=self.name,
            status_id=123
        )

        try:
            s = str(amolead)
        except TypeError as e:
            self.fail('Lead is not JSON serializable!')


