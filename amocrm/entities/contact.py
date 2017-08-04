import time
from copy import deepcopy

from ..dictwrap import DictWrap
from ..exceptions import MissingArgument
from ..fields import Field
from ..util import cast_to_cls_list

from .entity import Entity
from .lead import Lead


class Contact(Entity):

    def __init__(
            self,
            name=None,
            fields=None,
            tags=None,
            linked_leads=None,
            last_modified=None,
            **kwargs
        ):
        super().__init__(**kwargs)
        if not name:
            raise MissingArgument('Missing argument: "name"')
        # if not fields:
        #     raise MissingArgument('Missing argument: "fields"')

        if fields:
            fields = cast_to_cls_list(fields, Field)

        if tags:
            tags = self.normalize_tags(tags)

        if linked_leads:
            linked_leads = cast_to_cls_list(linked_leads, Lead)

        self.name = name
        self.fields = fields
        self.tags = tags
        self.linked_leads = linked_leads
        self.last_modified = last_modified

    def todict(self, verb='add', id_=None):
        self._dict = {
            "name": self.name,
        }

        if self.fields:
            self._dict.update({
                "custom_fields": [x.todict() for x in self.fields],
            })

        if self.tags:
            self._dict.update({
                'tags': ", ".join(self.tags)
            })

        if id_:
            self._dict.update({
                'id': id_,
            })

        last_modified = self.last_modified
        if verb == 'update' and not last_modified:
            last_modified = int(time.time())

        if last_modified:
            self._dict.update({
                'last_modified': last_modified
            })

        if self.linked_leads:
            linked_leads_with_ids = [l.id for l in self.linked_leads if l.id]
            if linked_leads_with_ids:
                self._dict.update({
                    'linked_leads_id': linked_leads_with_ids
                })

        d = {
            "request": {
                "contacts": {
                    verb: [
                        self._dict
                    ]
                }
            }
        }

        return deepcopy(d)
