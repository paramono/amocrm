import json
import pprint
import requests
from requests import Response
import xml.etree.ElementTree as etree

import amocrm.conf
from .entities import Entity, Contact, Lead
from .exceptions import (
    ResponseError,
    WrongStatusCode,
    NoCookieError,
    XmlReturnedFalse,
    NotAnEntity,
    WrongValueType
)
from .fields import (
    Field, 
    PhoneField,
    EmailField,
    NoteField,
    UrlField,
)
from .values import Value
from .util import Hasher


HEADERS = {
    'Content-Type': 'application/json'
}

amo_settings = amocrm.conf.settings


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
        if r.status_code != requests.codes.ok:
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

        # safeguard: tries to auth if no cookies found
        cookies = getattr(self, 'cookies', None)
        if not cookies:
            self.auth()

        r = requests.post(
            url, 
            cookies=cookies,
            headers=HEADERS, 
            data=entity_json,
        )

        if r.status_code != requests.codes.ok:
            raise ResponseError(
                'Failed to post an entity %s.\n'
                'Response:\n%s\n'
                '* * * * * * * * * *\n'
                'Data posted:\n%s' % (
                    entity_name,
                    self.prettify(r.text),
                    self.prettify(entity_json),
                )
            )

        entity_response_json = json.loads(r.text) 
        entity_returned = Hasher(entity_response_json)
        try:
            entity.id = int(
                entity_returned['response'][entity_name_plural]['add'][0]['id']
            )
        except ValueError:
            entity.id = None
        return r

    def prettify(self, data):
        if isinstance(data, Response):
            data = data.text
        elif isinstance(data, dict):
            data = str(data)

        if not isinstance(data, str):
            raise WrongValueType(
                'prettify accepts either str or Response objects'
                'you supplied object of type %s' % type(data)
            )

        parsed = json.loads(data)
        pretty = json.dumps(
            parsed, 
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
        return pretty

    def pprint(self, data):
        pretty = self.prettify(data)
        print(pritty)
