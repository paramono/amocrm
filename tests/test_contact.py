import unittest
from unittest import skip
from unittest.mock import patch

from amocrm.exceptions import *
from amocrm.models.entities.contact import Contact
from amocrm.models.field import (
    Field,
    PhoneField,
    EmailField,
    NoteField,
    UrlField,
)

from .base_field_value import BaseTest


class TestContact(BaseTest):

    def test_Contact_todict_returns_dict(self):
        amovalue = self.amovalue_phone
        amofield = PhoneField(
            # id_=self.amofield_id,
            values=amovalue,
            )
        amocontact = Contact(
            name=self.name,
            # fields=self.amofields,
            fields=amofield,
        )

        d = amocontact.todict()
        self.assertIsNotNone(d)
        self.assertIsInstance(d, dict)

    def test_Contact_accepts_one_Field(self):
        amovalue = self.amovalue_phone
        amofield = PhoneField(
            # id_=self.amofield_id,
            values=amovalue,
            )

        amocontact = Contact(
            name=self.name,
            # fields=self.amofields,
            fields=amofield,
        )

        self.assertEqual(
            amocontact.fields,
            [amofield]
        )

        d = amocontact.todict()
        self.assertEqual(d, {
            "request": {
                "contacts": {
                    "add": [{
                        "name": self.name, 
                        # "tags": user_tags, 
                        "custom_fields": [amofield.todict()]
                        # 'date_create': 1375105752, 
                        # 'company_name': 'amocrm', 
                        # 'linked_leads_id': [199402], 
                        # 'responsible_user_id': 10720146, 
                        # 'request_id': 1953, 
                        # 'last_modified': 1375105752
                    }]
                }
            }
        })


    def test_Contact_accepts_multiple_Fields(self):
        amovalue1 = self.amovalue_phone
        amofield1 = PhoneField(
            values=amovalue1,
            )

        amovalue2 = self.amovalue_email
        amofield2 = EmailField(
            values=amovalue2,
            )

        amofields = [amofield1, amofield2]

        amocontact = Contact(
            name=self.name,
            fields=amofields,
        )

        self.assertEqual(
            amocontact.fields,
            amofields
        )

        d = amocontact.todict()
        self.assertEqual(d, {
            "request": {
                "contacts": {
                    "add": [{
                        "name": self.name, 
                        # "tags": user_tags, 
                        "custom_fields": [
                            amofield1.todict(),
                            amofield2.todict(),
                        ]
                        # 'date_create': 1375105752, 
                        # 'company_name': 'amocrm', 
                        # 'linked_leads_id': [199402], 
                        # 'responsible_user_id': 10720146, 
                        # 'request_id': 1953, 
                        # 'last_modified': 1375105752
                    }]
                }
            }
        })

    def test_Contact_raises_on_empty_name(self):
        with self.assertRaises(MissingArgument):
            amocontact = Contact(
                fields=self.amofields,
            )

    def test_Contact_raises_on_empty_fields(self):
        with self.assertRaises(MissingArgument):
            amocontact = Contact(
                name=self.name,
            )

    def test_Contact_raises_on_wrong_fields(self):
        with self.assertRaises(WrongValueType):
            amocontact = Contact(
                name=self.name,
                fields="field",
            )

    def test_Contact_accepts_single_tag(self):
        tag = 'some tag'

        amocontact = Contact(
            name=self.name,
            fields=self.amofields,
            tags=tag,
        )

        self.assertEqual(
            amocontact.tags,
            [tag],
        )

        d = amocontact.todict()
        self.assertEqual(d, {
            "request": {
                "contacts": {
                    "add": [{
                        "name": self.name, 
                        # "tags": user_tags, 
                        "custom_fields": [x.todict() for x in self.amofields],
                        "tags": tag,
                        # 'date_create': 1375105752, 
                        # 'company_name': 'amocrm', 
                        # 'linked_leads_id': [199402], 
                        # 'responsible_user_id': 10720146, 
                        # 'request_id': 1953, 
                        # 'last_modified': 1375105752
                    }]
                }
            }
        })

    
    def test_Contact_accepts_multiple_tags_as_list(self):
        tags = ['master', 'amo']

        amocontact = Contact(
            name=self.name,
            fields=self.amofields,
            tags=tags
        )

        self.assertEqual(
            amocontact.tags,
            tags,
        )

        d = amocontact.todict()
        self.assertEqual(d, {
            "request": {
                "contacts": {
                    "add": [{
                        "name": self.name, 
                        # "tags": user_tags, 
                        "custom_fields": [x.todict() for x in self.amofields],
                        "tags": ", ".join(tags),
                        # 'date_create': 1375105752, 
                        # 'company_name': 'amocrm', 
                        # 'linked_leads_id': [199402], 
                        # 'responsible_user_id': 10720146, 
                        # 'request_id': 1953, 
                        # 'last_modified': 1375105752
                    }]
                }
            }
        })

    def test_Contact_accepts_multiple_tags_as_str(self):
        tags = 'master,amo'

        amocontact = Contact(
            name=self.name,
            fields=self.amofields,
            tags=tags
        )

        expected_result = ['master', 'amo']

        self.assertEqual(
            amocontact.tags,
            expected_result,
        )

        d = amocontact.todict()
        self.assertEqual(d, {
            "request": {
                "contacts": {
                    "add": [{
                        "name": self.name, 
                        # "tags": user_tags, 
                        "custom_fields": [x.todict() for x in self.amofields],
                        "tags": ', '.join(expected_result),
                        # 'date_create': 1375105752, 
                        # 'company_name': 'amocrm', 
                        # 'linked_leads_id': [199402], 
                        # 'responsible_user_id': 10720146, 
                        # 'request_id': 1953, 
                        # 'last_modified': 1375105752
                    }]
                }
            }
        })

    def test_Contact_links_leads(self):
        self.fail()

    def test_Contact_is_json_serializable(self):
        amovalue = self.amovalue_phone
        amofield = Field(
            id_=self.amofield_id,
            values=amovalue,
            )

        amocontact = Contact(
            name=self.name,
            # fields=self.amofields,
            tags=['master', 'amo'],
            fields=amofield,
        )

        try:
            s = str(amocontact)
        except TypeError as e:
            self.fail('Contact is not JSON serializable!')

    def test_Contact_normalize_tags_single_str_tag(self):
        tags = 'tag'
        normalized = Contact.normalize_tags(tags)
        self.assertEqual(
            [tags],
            normalized
        )

    def test_Contact_normalize_tags_multiple_str_tag(self):
        tags = 'tag1, tag2, tag3 '
        normalized = Contact.normalize_tags(tags)

        expected_result = ['tag1', 'tag2', 'tag3']
        self.assertEqual(
            expected_result,
            normalized
        )

    def test_Contact_normalize_tags_list(self):
        tags = ['tag1', 'tag2', 'tag3']
        normalized = Contact.normalize_tags(tags)
        self.assertEqual(
            tags,
            normalized,
        )
