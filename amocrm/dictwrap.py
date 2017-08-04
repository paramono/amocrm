import json
from copy import deepcopy


class DictWrap:
    ALLOWED_DICT_KEYS = ('value', 'enum',)

    def __init__(self, **kwargs):
        self.__dict__['_dict'] = {}

    def todict(self):
        return deepcopy(self._dict)

    def tojson(self, verb='add', id_=None):
        return json.dumps(self.todict(verb=verb, id_=id_))

    def __setitem__(self, key, value):
        self._dict[key] = value
        
    def __getitem__(self, key):
        return self._dict[key]

    def __repr__(self):
        # return repr(self.todict())
        return repr(self._dict)

    def __delitem__(self, key):
        del self._dict[key]

    def clear(self):
        return self._dict.clear()

    def copy(self):
        return self._dict.copy()

    def has_key(self, key):
        return self._dict.has_key(k)
    
    def pop(self, k, d=None):
        self._dict.pop(k, d)

    def update(self, *args, **kwargs):
        return self._dict.update(*args, **kwargs)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def __cmp__(self, d):
        return cmp(self._dict, d)

    def __contains__(self, item):
        return item in self._dict

    def __iter__(self):
        return iter(self._dict)

    def __unicode__(self):
        return unicode(repr(self._dict))

    def __call__(self):
        return self.todict()

    def __str__(self):
        return json.dumps(
            self.todict(), 
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
        )
