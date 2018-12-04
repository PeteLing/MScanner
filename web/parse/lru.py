# coding=utf-8

import threading


class Node:
    __slots__ = ['prev', 'next', 'me']

    def __init__(self, prev, me):
        self.prev = prev
        self.me = me
        self.next = None


class LRU:
    def __init__(self, count, pairs=None):
        if pairs is None:
            pairs = []
        self.lock = threading.RLock()
        self.count = max(count, 1)
        self.d = {}
        self.first = None
        self.last = None
        for key, value in pairs:
            self[key] = value

    def __contains__(self, item):
        for it in self.d:
            if item == it.me[0]:
                return True
        # return item in self.d
        return False

    def __getitem__(self, item):
        with self.lock:
            it = self.d[item].me
            self[it[0]] = it[1]
            return it[1]

    def __setitem__(self, key, value):
        with self.lock:
            for k, v in self.d.items():
                if key == k:
                    del self[key]
            # if key in self.d:
            #     del self[key]
            nobj = Node(self.last, (key, value))
            if self.first is None:
                self.first = nobj
            if self.last:
                self.last.next = nobj
            self.last = nobj
            self.d[nobj] = nobj
            if len(self.d) > self.count:
                if self.first == self.last:
                    self.first = None
                    self.last = None
                    return
                item = self.first
                item.next.prev = None
                self.first = item.next
                item.next = None
                # del self.d[item.me[0]]
                del self.d[item]
                del item

    def __delitem__(self, obj):
        with self.lock:
            nobj = self.d[obj]
            if nobj.prev:
                nobj.prev.next = nobj.next
            else:
                self.first = nobj.next
            if nobj.next:
                nobj.next.prev = nobj.prev
            else:
                self.last = nobj.prev
            del self.d[obj]

    def __iter__(self):
        cur = self.first
        while cur is not None:
            cur2 = cur.next
            yield cur.me[1]
            cur = cur2

    def iteritems(self):
        cur = self.first
        while cur is not None:
            cur2 = cur.next
            yield cur.me
            cur = cur2

    def iterkeys(self):
        return iter(self.d)

    def itervalues(self):
        for i, j in self.iteritems():
            yield j

    def keys(self):
        return self.d.keys()

    def __len__(self):
        return len(self.d)

    def values(self):
        return [i.me[1] for i in self.d.values()]


if __name__ == '__main__':
    lru_test = LRU(4)
    lru_test['1'] = 1
    lru_test['2'] = 1
    lru_test['3'] = 1
    lru_test['4'] = 1
    lru_test['5'] = 1
    for i in range(6):
        print(i, str(i) in lru_test)
