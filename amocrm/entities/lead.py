from copy import deepcopy

from ..exceptions import MissingArgument
from ..dictwrap import DictWrap
from ..fields import Field
from ..util import cast_to_cls_list

from .entity import Entity


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
