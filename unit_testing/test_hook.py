import socket
import time
import requests


def _hook_manager():
    _connect = socket.socket.connect
    socket.socket.connect = lambda *args, **kwargs: _hook_connect((_connect, args, kwargs), )


def _hook_connect(*args, **kwargs):
    '''
    '''
    _conn = 0
    _time = 0
    _speed = 20
    realfun, realargs, realkwargs = args[0]
    while True:
        begin = time.time()
        now_time = max(0.01, begin - _time)
        if now_time > 5:
            _conn = 0
            _time = now_time
            break
        if _conn // now_time <= _speed:
            break
        else:
            time.sleep(0.01)
    _conn += 1
    print('Hook ....')
    # return apply(realfun, *realargs, **realkwargs))
    return realfun(*realargs, **realkwargs)


if __name__ == '__main__':
    _hook_manager()
    for i in range(10):
        print(requests.get('http://www.baidu.com'))

