def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj


def dictify(obj, key):
    if not isinstance(obj, dict):
        return {key: obj}
    return obj
