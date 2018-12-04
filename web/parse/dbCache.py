# coding=utf-8

import threading

from web.parse.documentParser import documentParser
from web.parse.lru import LRU


class dpCache:

    def __init__(self):
        self._cache = LRU(30)
        self._LRULock = threading.RLock()

    def getDocumentParserFor(self, Response):
        res = None
        hash_string = hash(Response.body)

        with self._LRULock:
            if hash_string in self._cache:
                res = self._cache[hash_string]
            else:
                res = documentParser(Response)
                self._cache[hash_string] = res
            return res


dpc = dpCache()
