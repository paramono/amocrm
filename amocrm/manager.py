import json
import pprint
import requests
import xml.etree.ElementTree as etree

import amocrm.conf
from amocrm.models.field import (
    Field, 
    PhoneField,
    EmailField,
    NoteField,
    UrlField,
)
from amocrm.models.value import Value
from amocrm.models.entities.entity import Entity
from amocrm.models.entities.contact import Contact
from amocrm.models.entities.lead import Lead
from amocrm.util import Hasher
from amocrm.exceptions import *


HEADERS = {
    'Content-Type': 'application/json'
}

amo_settings = amocrm.conf.settings


class ResponseError(RuntimeError):    pass
class AuthFailed(ResponseError):      pass
class WrongStatusCode(ResponseError): pass
class NoCookieError(AuthFailed):      pass
class XmlReturnedFalse(AuthFailed):   pass


class Manager(object):

    def __init__(self):
        pass

    def auth(self):
        r = requests.post(
            amocrm.conf.settings.URL_POST_AUTH,
            data=amocrm.conf.settings.AUTH_DATA,
            )

        # raises 404 on wrong URL_POST_AUTH
        # if AUTH_DATA is wrong, status_code will be 200,
        # but the returned xml will have <auth>false</auth>
        # r.raise_for_status()
        if r.status_code != 200:
            raise WrongStatusCode(
                'Authentication error! Status code is %s ' 
                'should be 200' % r.status_code
            )

        self.cookies = r.cookies # auth cookie
        if not self.cookies:
            raise NoCookieError(
                "Authentication error! Cookies are empty".format(r.status_code)
            )

        #parsing xml response
        tree = etree.fromstring(r.text)
        if tree[0].text != "true":
            raise XmlReturnedFalse(
                "Authentication error! XML has no 'true'".format(r.status_code)
            )
        return r

    def get_account_info(self):
        r = requests.get(
            amo_settings.URL_GET_ACCOUNT,
            cookies=self.cookies,
            headers=HEADERS,
            )
        r.raise_for_status()
        return r

    def get_leads(self):
        r = requests.get(
            amo_settings.URL_GET_LEADS,
            cookies=self.cookies,
            headers=HEADERS,
            )
        r.raise_for_status()
        return r

    def get_contacts(self):
        r = requests.get(
            amo_settings.URL_GET_CONTACTS,
            cookies=self.cookies,
            headers=HEADERS,
            )
        r.raise_for_status()
        return r

    def post_entity(self, entity):
        if isinstance(entity, Entity):
            entity_json = entity.tojson()
        else:
            raise NotAnEntity(
                'You supplied object of %s, '
                'expected Entity instead' % type(entity)
            )


        entity_name = entity.__class__.__name__.lower()
        entity_name_plural = entity_name + 's'

        url = amocrm.conf.settings.get_entity_url(
            'post',
            entity_name_plural,
        )
        cookies = getattr(self, 'cookies', None)

        r = requests.post(
            url, 
            cookies=cookies,
            headers=HEADERS, 
            data=entity_json,
        )
        r.raise_for_status()

        entity_response_json = json.loads(r.text) 
        entity_returned = Hasher(entity_response_json)
        try:
            entity.id = int(
                entity_returned['response'][entity_name_plural]['add'][0]['id']
            )
        except ValueError:
            entity.id = None
        return r

    def post_lead(self, entity):
        if isinstance(entity, Lead):
            json_data = entity.tojson()

        r = requests.post(
            amocrm.conf.settings.URL_POST_LEADS, 
            cookies=self.cookies,
            headers=HEADERS, 
            data=json_data,
            )
        # getting entity id for response
        # (required for linked leads)
        entity_json = json.loads(r.text) 
        entity_json = Hasher(entity_json)
        try:
            entity.id = int(
                entity_json['response']['leads']['add'][0]['id']
            )
        except ValueError:
            entity.id = None
        return r

    def post_contact(self, entity):
        if isinstance(entity, Contact):
            json_data = entity.tojson()

        r = requests.post(
            amocrm.conf.settings.URL_POST_CONTACTS, 
            cookies=self.cookies,
            headers=HEADERS, 
            data=json_data,
            )

        # getting entity id for response
        # (required for linked leads)
        entity_json = json.loads(r.text) 
        entity_json = Hasher(entity_json)
        entity_id = entity_json['response']['contacts']['add'][0]['id']
        entity.id = entity_id

        return r

    def pprint(self, response):
        parsed = json.loads(response.text)
        pretty = json.dumps(
            parsed, 
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
        print(pretty)
        # pprint.pprint(parsed, indent=1)

