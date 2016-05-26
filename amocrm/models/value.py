from amocrm.dictwrap import DictWrap
from amocrm.exceptions import *


class Value(DictWrap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not kwargs.get('value'):
            raise MissingValue(
                'AmoValue needs to have a "value" key in arguments'
            )
        self._dict = kwargs
        # self.__dict__.update(**kwargs)
