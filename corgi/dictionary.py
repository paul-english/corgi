def rename_keys(dictionary, names_map):
    for k, v in names_map.iteritems():
        if k not in dictionary:
            continue
        dictionary[v] = dictionary[k]
        del dictionary[k]
    return dictionary
