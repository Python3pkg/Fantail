"""
Fantail
"""
# -*- coding: utf-8 -*-
from __future__ import print_function

import collections
import inspect


class Fantail(dict):
    def __init__(self, *a, **kw):
        dict.__init__(self)

        for item in a:
            if inspect.isclass(item):
                continue
            elif isinstance(item, dict):
                self.update(item)
            else:
                print(item, isinstance(item, Fantail))
                raise Exception("invalid init argument: {}".format(str(item)))
        self.update(kw)

    def __setitem__(self, key, value):
        if isinstance(key, str) and '.' in key:
            keyA, keyB = key.split('.', 1)
            self[keyA][keyB] = value
        elif isinstance(value, dict) and len(value) > 0:
            self[key].update(value)
        else:
            dict.__setitem__(self, key, value)

    def get(self, key, default=None):
        if isinstance(key, str) and '.' in key:
            keyA, keyB = key.split('.', 1)
            if not keyA in self:
                return default
            return self[keyA].get(keyB, default)
        else:
            return dict.get(self, key, default)

    def __getitem__(self, key):
        if isinstance(key, str) and '.' in key:
            keyA, keyB = key.split('.', 1)
            return self[keyA][keyB]

        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        self[key] = Fantail()
        return self[key]

    def __reduce__(self):
        return type(self), (Fantail, ), None, None, iter(self.items())

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(Fantail, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(Fantail,
                          copy.deepcopy(self.items()))

    def update(self, d=None, **kwargs):
        if d is None:
            pass
        elif isinstance(d, dict):
            for k, v in d.items():
                self[k] = v
        if len(kwargs):
            self.data.update(kwargs)
