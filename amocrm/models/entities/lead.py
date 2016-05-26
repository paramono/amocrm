from copy import deepcopy

from amocrm.exceptions import MissingArgument
from amocrm.dictwrap import DictWrap
from amocrm.models.entities.entity import Entity
from amocrm.models.field import Field
from amocrm.util import cast_to_cls_list


class Lead(Entity):

    def __init__(self, name=None, status_id=None, **kwargs):
        super().__init__(**kwargs)
        if not name:
            raise MissingArgument('Missing argument: "name"')
        if not status_id:
            raise MissingArgument('Missing argument: "status_id"')

        self.name = name
        self.status_id = status_id

    def todict(self):
        self._dict = {
            "name": self.name,
            "status_id": self.status_id,
        }

        d = {
            "request":  {
                "leads":  {
                    "add":  [
                        self._dict
                    ]
                }
            }
        }

        return deepcopy(d)
