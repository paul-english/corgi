def listify(obj):
    if isinstance(obj, list) or isinstance(obj, tuple):
        return obj
    return [obj]


def dictify(obj, key):
    if isinstance(obj, dict):
        return obj
    return {key: obj}
