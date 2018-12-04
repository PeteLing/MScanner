# coding=utf-8

from urllib.parse import urlparse
from urllib.parse import parse_qs

DEFAULT_ENCODING = "UTF-8"


class data(dict):
    def __init__(self, init_val=(), encoding=DEFAULT_ENCODING):
        dict.__init__(self)
        self.encoding = encoding

        if isinstance(init_val, data):
            dict.update(self, init_val)
        elif isinstance(init_val, str):
            for k, v in parse_qs(init_val).items():
                self[k] = v[0]
        else:
            for item in init_val:
                try:
                    key, val = item
                except TypeError:
                    raise TypeError
                self[key] = val


if __name__ == '__main__':
    a = data("user=1&password=2")
    print(a)