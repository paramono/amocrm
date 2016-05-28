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
            **kwargs
        ):
        super().__init__(**kwargs)
        if not name:
            raise MissingArgument('Missing argument: "name"')
        if not fields:
            raise MissingArgument('Missing argument: "fields"')

        fields = cast_to_cls_list(fields, Field)

        if tags:
            tags = self.normalize_tags(tags)

        if linked_leads:
            linked_leads = cast_to_cls_list(linked_leads, Lead)

        self.name = name
        self.fields = fields
        self.tags = tags
        self.linked_leads = linked_leads

    @classmethod
    def normalize_tags(cls, tags):
        if isinstance(tags, str):
            tags = tags.split(',')
            for i, _ in enumerate(tags):
                tags[i] = tags[i].strip()
            
        elif isinstance(tags, list):
            pass
        return tags

    def todict(self):
        self._dict = {
            "name": self.name,
            "custom_fields": [x.todict() for x in self.fields],
            # "custom_fields": self.fields,
        }

        if self.tags:
            self._dict.update({
                'tags': ", ".join(self.tags)
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
                    "add": [
                        self._dict
                    ]
                }
            }
        }

        return deepcopy(d)
