def pipe(*functions):
    def closure(x):
        for fn in functions:
            if not out:
                out = fn(x)
            else:
                out = fn(out)
        return out

    return closure
