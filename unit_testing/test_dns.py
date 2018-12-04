# coding=utf-8

import socket

_dnscache = {}


def _setDNSCache():
    def igetaddrinfo(*args, **kwargs):
        if args in _dnscache:
            return _dnscache[args]
        else:
            _dnscache[args] = socket.igetaddrinfo(*args, **kwargs)
            return _dnscache[args]
    if not hasattr(socket, 'igetaddrinfo'):
        socket.igetaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = igetaddrinfo


def test():
    _setDNSCache()
    import requests
    r1 = requests.get('http://www.baidu.com')
    print('第一次没有命中缓存时间: ' + str(r1.elapsed.microseconds))
    # print(_dnscache)
    r2 = requests.get('http://www.baidu.com')
    print('第二次命中缓存时间: ' + str(r2.elapsed.microseconds))


if __name__ == '__main__':
    test()