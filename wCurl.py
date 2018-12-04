# coding=utf-8

import socket
import http.client
import requests
import time
import random

from web.http.config import cfg
from web.http.URL import URL
from web.http.Response import Response, from_requests_response

timeout = 60
socket.setdefaulttimeout(timeout)
DEBUGSWITCH = 0  # 0 关闭调试， 1 开启调试


class wCurl:
    def __init__(self):
        self._time = 0.0
        self._speed = 20
        self._conn = 0
        self._hook_manager()
        self._scan_signature = cfg['scan_signature'] if cfg.get('scan_signature') is not None else "MFYScanner/1.0"
        self._scan_cookeis = cfg['scan_cookies'] if cfg.get('scan_cookies') is not None else {}
        self._scan_proxies = cfg['scan_proxies'] if cfg.get('scan_proxies') is not None else {}

        # 0关闭调试、 1开启调试
        http.client.HTTPConnection.debuglevel = DEBUGSWITCH

    def _hook_manager(self):
        _connect = socket.socket.connect
        # socket.socket.connect = lambda *args, **kwargs: apply(self._hook_connect, (_connect, self, args, kwargs))
        socket.socket.connect = lambda *args, **kwargs: self._hook_connect((_connect, self, args, kwargs))

    def _hook_connect(self, *args, **kwargs):
        '''
        '''
        realfun, selfobj, realargs, realkwargs = args[0]
        while True:
            # begin = time.time()
            # now_time = max(0.01, begin - self._time)
            # if now_time > 5:
            #     self._conn = 0
            #     self._time = now_time
            # if self._conn // now_time <= self._speed:
            #     break
            # else:
            #     time.sleep(0.01)
            time.sleep(0.1)
            break
        # self._conn += 1
        # return apply(realfun, *realargs, **realkwargs))
        return realfun(*realargs, **realkwargs)

    def get_default_headers(self, headers):
        default_headers = {"User-Agent": self._scan_signature}
        if headers is None:
            return default_headers
        default_headers.update(headers)
        return default_headers

    def get(self, url, headers=None, **kwargs):
        default_headers = self.get_default_headers(headers)
        if not isinstance(url, URL):
            url = URL(url)
        requests_response = None
        try:
            requests_response = requests.get(url.url_string, headers=default_headers, **kwargs)
        except:
            return self._make_response(requests_response, url)
        response = self._make_response(requests_response, url)
        return response

    def post(self, url, headers=None, data=None, **kwargs):
        default_headers = self.get_default_headers(headers)
        if not isinstance(url, URL):
            url = URL(url)
        requests_response = None
        try:
            requests_response = requests.post(url.url_string, headers=default_headers, data=data, **kwargs)
        except:
            return self._make_response(requests_response, url)
        response = self._make_response(requests_response, url)
        return response

    def __getattr__(self, name):
        print(name)

    def _send_req(self, req):
        method = req.get_method()
        # 不带查询参数和信息片段的URL
        uri = req.get_url().get_uri_string()
        querystring = req.get_get_param()
        postdata = req.get_post_param()
        headers = req.get_headers()
        cookeis = self._scan_cookeis
        proxies = self._scan_proxies
        send = getattr(requests, method.lower())
        requests_response = None
        try:
            # requests_response = send(uri, params=querystring, data=postdata, headers=headers, cookeis=cookeis,
            #                          proxies=proxies)
            requests_response = send(uri)
        except:
            return self._make_response(requests_response, req.get_url())
        else:
            response = self._make_response(requests_response, req.get_url())
            return response

    def _make_response(self, resp_from_requests, req_url):
        if resp_from_requests is None:
            response = Response(req_url=req_url)
        else:
            response = from_requests_response(resp_from_requests, req_url)
        return response


wcurl = wCurl()
