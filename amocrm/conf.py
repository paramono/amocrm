import re

from amocrm.dictwrap import DictWrap


AMO_POSTFIX_GET_ACCOUNT   = "/private/api/v2/json/accounts/current"
AMO_POSTFIX_GET_LEADS     = "/private/api/v2/json/leads/list"
AMO_POSTFIX_GET_CONTACTS  = "/private/api/v2/json/contacts/list"

AMO_POSTFIX_POST_AUTH     = "/private/api/auth.php"
AMO_POSTFIX_POST_LEADS    = "/private/api/v2/json/leads/set"
AMO_POSTFIX_POST_CONTACTS = "/private/api/v2/json/contacts/set"


__all__ = ['amo_settings', 'AmoSettings']


class AmoSettings(DictWrap):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dict = kwargs
        self.api_links = {
            'get': {
                'account':  AMO_POSTFIX_GET_ACCOUNT,
                'leads':    AMO_POSTFIX_GET_LEADS,
                'contacts': AMO_POSTFIX_GET_CONTACTS,
            },
            'post': {
                'auth':     AMO_POSTFIX_POST_AUTH,
                'leads':    AMO_POSTFIX_POST_LEADS,
                'contacts': AMO_POSTFIX_POST_CONTACTS,
            },
        }

    def __getattr__(self, name):
        pattern = '^URL_(GET|POST)_([A-Z]+)$'
        m = re.match(pattern, name)
        if not m: # regular attributes
            return self._dict.get(name)

        # URL attributes
        method  = m.group(1).lower() 
        entity  = m.group(2).lower()
        postfix = self.get_postfix(method, entity)
        url     = self.get_url(postfix)
        return url

    def __setattr__(self, name, value):
        self.__dict__['_dict'][name] = value

    def get_postfix(self, method, entity):
        return self.api_links[method][entity]

    def get_entity_url(self, method, entity):
        postfix = self.get_postfix(method, entity)
        url     = self.get_url(postfix)
        return url

    def get_url(self, postfix):
        if not self.USER_DOMAIN: 
            raise AttributeError(
                'USER_DOMAIN must be specified for amocrm settings'
            )
        return '%s%s' % (self.USER_DOMAIN, postfix)

    @property
    def AUTH_DATA(self):
        return {
            "USER_LOGIN": self.USER_LOGIN,
            "USER_HASH":  self.USER_HASH,
            "type":       "json",
        }
        
settings = AmoSettings()
