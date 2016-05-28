import unittest
from unittest import skip
from unittest.mock import patch

import amocrm.conf

from .base_copysettings import BaseCopySettings


class SettingsTest(BaseCopySettings):

    def test_get_url(self):

        arg = '/whatever'
        self.set_domain()

        self.assertEqual(
            self.conf.get_url(arg),
            self.domain + arg,
            )

    def test_get_url_raises_if_no_domain(self):
        arg = '/whatever'

        with self.assertRaises(AttributeError):
            self.conf.USER_DOMAIN
            self.conf.get_url(arg)

    def test_setitem(self):
        self.conf['USER_DOMAIN'] = self.domain

        self.assertEqual(
            self.conf.USER_DOMAIN,
            self.conf['USER_DOMAIN'],
        )

    def test_setattr(self):
        self.conf.USER_DOMAIN = self.domain

        self.assertEqual(
            self.conf.USER_DOMAIN,
            self.conf['USER_DOMAIN'],
        )

    def test_URL_AUTH(self):
        self.set_domain()

        self.assertEqual(
            self.conf.URL_POST_AUTH,
            self.domain + amocrm.conf.AMO_POSTFIX_POST_AUTH
            )

    def test_AUTH_DATA(self):
        self.set_domain()
        self.set_auth_data()

        self.assertEqual(
            self.conf.AUTH_DATA,
            {
                'USER_LOGIN': self.user_login,
                'USER_HASH': self.user_hash,
                'type': 'json',
            }
        )

    # assertEqual(attr, 
    def test_get_postfix(self):
        for method, method_dict in self.conf.api_links.items():
            for entity, postfix in method_dict.items():
                self.assertEqual(
                    self.conf.api_links[method][entity],
                    self.conf.get_postfix(method, entity)
                )

    def test_getattr_url_attrs(self):
        self.set_domain()
        for method, method_dict in self.conf.api_links.items():
            for entity, postfix in method_dict.items():
                attr = getattr(
                    self.conf,
                    'URL_%s_%s' % (method.upper(), entity.upper(),)
                )

                full_url = self.conf.USER_DOMAIN + \
                    self.conf.api_links[method][entity]
                self.assertEqual(
                    attr,
                    full_url,
                )
