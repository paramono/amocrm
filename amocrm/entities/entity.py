from amocrm.dictwrap import DictWrap


class Entity(DictWrap):

    @classmethod
    def normalize_tags(cls, tags):
        if isinstance(tags, str):
            tags = tags.split(',')
            for i, _ in enumerate(tags):
                tags[i] = tags[i].strip()
            
        elif isinstance(tags, list):
            pass
        return tags

