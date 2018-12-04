# coding=utf-8

import copy
from web.http.URL import URL
import uuid

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.102 Safari/537.36",


class Request:
    def __init__(self, url, method='GET', headers=None, cookies=None, referer=None,
                data=None, user_agent=DEFAULT_USER_AGENT, **kwargs):
        if isinstance(url, URL):
            self._url = url
        else:
            self._url = URL(url)
        self._method = method.upper()
        self.id = uuid.uuid1()
        self._headers = headers if headers is not None else {}
        self._cookies = cookies
        self._referer = referer
        self._user_agent = user_agent
        if self._cookies:
            self._headers.update({"Cookie": self._cookies})
        if self._referer:
            self._headers.update({"Referer": self._referer})
        if self._user_agent:
            self._headers.update({"User-Agent": self._user_agent})
        self._get_data = self._url.get_query()
        self._post_data = data if data else ""

    def get_id(self):
        return self.id

    def get_get_param(self):
        return self._get_data

    def get_post_param(self):
        return self._post_data

    def get_url(self):
        return self._url

    def get_method(self):
        return self._method

    def get_headers(self):
        return self._headers

    def get_cookies(self):
        return self._cookies

    def set_method(self, method):
        self._method = method

    def set_post_data(self, postdata):
        self._post_data = postdata

    def set_get_data(self, getdata):
        self._get_data = getdata

    def set_referer(self, referer):
        self._referer = referer

    def set_cookies(self, cookies):
        self._cookies = cookies

    def __eq__(self, other):
        if self._url == other._url and self._method == other._method:
            return True
        else:
            return False

    def __str__(self):
        result_string = self._method
        result_string += " " + self._url.url_string + " HTTP/1.1\r\n"
        headers = copy.deepcopy(self._headers)
        headers.update({"host": self._url.get_host()})
        for key, value in headers.items():
            result_string += key + ": " + value
            result_string += "\r\n"
        result_string += "\r\n"
        if self._method == "POST":
            result_string += str(self._post_data)
        result_string = result_string
        return result_string

    def __repr__(self):
        vals = {'method': self.get_method(), 'url': str(self.get_url()), 'id': self.get_id()}
        return '<Request | %(method)s | %(url)s | %(id)s>' % vals

    def __hash__(self):
        return hash(self.id)


if __name__ == '__main__':
    req = Request("http://www.baidu.com/index.php?id=1")
    print('id: ', req.get_id())
    print('url:', req.get_url())
    print('get param: ', req.get_get_param())
    print('post param: ', req.get_post_param())
    print('method: ', req.get_method())
    print('headers: ', req.get_headers())
    print('cookies: ', req.get_cookies())

    # print('Request: ', req)

