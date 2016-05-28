from copy import deepcopy

import amocrm.conf
from .dictwrap import DictWrap
from .exceptions import (
    MissingArgument,
    EmptyArgument,
    WrongValueType,
)
from .util import (
    cast_to_cls_list,
    is_list_of_class,
)
from .values import Value


class Field(DictWrap):
    ALLOWED_ROOT_EXTRA_KEYS  = ('name',  'code',)
    # ALLOWED_VALUE_KEYS = ('value', 'enum',)
    ALLOWED_DICT_KEYS = ('value', 'enum',)

    def __init__(self, id_=None, values=None, type=None, **kwargs):
        super().__init__(**kwargs)

        id_ = id_ or self.get_id()
        if not id_:
            raise MissingArgument('Missing argument: "id"')
        if not values:
            raise MissingArgument('Missing argument: "values"')

        # values = cast_to_cls_list(values, Value)
        values = self.cast_values(values, Value)

        self.id_ = id_
        self.values = values
        self.extra  = kwargs

    @classmethod
    def get_enum(cls):
        return amocrm.conf.settings.DEFAULT_ENUM

    @classmethod
    def get_id(cls):
        return 

    @classmethod
    def cast_values(cls, attr, target_cls):
        if not attr:
            raise EmptyArgument

        if isinstance(attr, target_cls):
            attr = [attr]
        elif isinstance(attr, dict):
            # converting dict of values to
            # instance of class
            inst = target_cls(**attr)
            # putting this instance to list
            attr = [inst]
        elif isinstance(attr, str):
            # converting string of values to dict
            d = {'value': attr}
            # converting dict of values to
            # instance of class
            inst = target_cls(**d)
            # putting this instance to list
            attr = [inst]
        elif isinstance(attr, list):
            if is_list_of_class(attr, target_cls):
                pass
            elif is_list_of_class(attr, dict):
                attr = [target_cls(**d) for d in attr]
        else:
            raise WrongValueType(
                'You supplied %s, but %s was expected' % (
                    type(attr),
                    target_cls.__name__,
                )
            )

        enum = cls.get_enum()
        if enum:
            for v in attr:
                v['enum'] = enum
        return attr


    def todict(self):
        self._dict = {
            "id"    : self.id_,
            "values": [x.todict() for x in self.values],
        }

        # update data dict with optional values ('name', 'code', etc.)
        self._dict.update(
            self._build_root_extra_dict(self.extra)
        )
        return deepcopy(self._dict)

    def _build_root_extra_dict(self, extra):
        return {k:v for k,v in extra.items() if k in self.ALLOWED_ROOT_EXTRA_KEYS}


class PhoneField(Field):

    @classmethod
    def get_enum(cls):
        return amocrm.conf.settings.PHONE_DEFAULT_ENUM

    @classmethod
    def get_id(cls):
        return amocrm.conf.settings.PHONE_ID


class EmailField(Field):

    @classmethod
    def get_enum(cls):
        return amocrm.conf.settings.EMAIL_DEFAULT_ENUM

    @classmethod
    def get_id(cls):
        return amocrm.conf.settings.EMAIL_ID


class UrlField(Field):

    @classmethod
    def get_enum(cls):
        return amocrm.conf.settings.URL_DEFAULT_ENUM

    @classmethod
    def get_id(cls):
        return amocrm.conf.settings.URL_ID


class NoteField(Field):

    @classmethod
    def get_enum(cls):
        return amocrm.conf.settings.NOTE_DEFAULT_ENUM

    @classmethod
    def get_id(cls):
        return amocrm.conf.settings.NOTE_ID
