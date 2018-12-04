# coding=utf-8

import web.http.encode_decode as enc_dec
from web.http.data import data

DEFAULT_ENCODING = "utf-8"


class querystring(data):

    def __init__(self, init_val=(), strict=False, encoding=DEFAULT_ENCODING):
        super().__init__(init_val, encoding)

    def __str__(self):
        return enc_dec.urlencode(self, encoding=self.encoding)


if __name__ == '__main__':
    a = querystring([("a", [2, 3])])
    print(a)