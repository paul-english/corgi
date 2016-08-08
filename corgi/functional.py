import collections
import functools


def pipe(*functions):
    def closure(x):
        out = None
        for fn in functions:
            if out is None:
                out = fn(x)
            else:
                out = fn(out)
        return out

    return closure


class memoize(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(compose2, fs)


class thunk(object):
    """Printable thunk object for ensuring things are callable"""

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return "<thunk %s>" % self.x

    def __call__(self, *args, **kwargs):
        if hasattr(self.x, '__call__'):
            return self.x(*args, **kwargs)
        return self.x
