import time
from copy import deepcopy

from ..exceptions import MissingArgument
from ..dictwrap import DictWrap
from ..fields import Field
from ..util import cast_to_cls_list

from .entity import Entity


class Customer(Entity):

    def __init__(
        self, name=None, next_date=None,
        contact_id=None, tags=None, **kwargs
    ):
        super().__init__(**kwargs)
        if not name:
            raise MissingArgument('Missing argument: "name"')

        if tags:
            tags = self.normalize_tags(tags)

        if not next_date:
            next_date = int(time.time())

        self.name = name
        self.tags = tags
        self.next_date = next_date
        self.contact_id = contact_id

    def todict(self, verb='add', id_=None):
        self._dict = {
            "name": self.name,
            # "status_id": self.status_id,
        }

        if self.tags:
            self._dict.update({
                'tags': ", ".join(self.tags)
            })

        if self.next_date:
            self._dict.update({
                'next_date': self.next_date
            })

        if self.contact_id:
            self._dict.update({
                'main_contact_id': self.contact_id
            })

        d = {
            "request":  {
                "customers":  {
                    "add":  [
                        self._dict
                    ]
                }
            }
        }

        return deepcopy(d)
