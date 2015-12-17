def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj


def dictify(obj, key):
    if isinstance(obj, dict):
        return obj
    return {key: obj}
