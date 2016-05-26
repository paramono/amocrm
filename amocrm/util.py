from amocrm.exceptions import WrongValueType, ForbiddenValueKey


class Hasher(dict):
    # http://stackoverflow.com/a/3405143/190597
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def is_list_of_class(list_, cls, allowed_keys=None):
    for d in list_:
        if not isinstance(d, cls):
            return False
            # raise WrongValueType(
            #     'Your list of values should contain '
            #     '%s instances only' % cls.__name__
            # )
        if allowed_keys:
            for k in d.keys():
                if k not in allowed_keys:
                    raise ForbiddenValueKey(
                        'Key "%s" not allowed in value dicts' % k
                    )
    return True


def cast_to_cls_list(attr, cls):
    if not attr:
        raise EmptyArgument

    if isinstance(attr, cls):
        attr = [attr]
    elif isinstance(attr, list):
        try:
            is_list_of_class(attr, cls)
        except WrongValueType as e:
            raise e
    else:
        raise WrongValueType(
            'You supplied %s, but %s was expected' % (
                type(attr),
                cls.__name__,
            )
        )
    return attr
