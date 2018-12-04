# coding=utf-8

import uuid
import re
import requests


DEFAULT_ENCODING = "utf-8"
DEFAULT_CHARSET = DEFAULT_ENCODING
CR = '\r'
LF = '\n'
CRLF = CR+LF
SP = ' '


# 将Requests模块返回的响应转换为Response类
def from_requests_response(res, req_url):
    code = res.status_code
    msg = res.reason
    headers = res.headers
    body = res.content
    real_url = res.url
    charset = res.encoding
    return Response(code, headers, body, req_url, real_url, msg, charset=charset)


class Response:
    def __init__(self, status_code=None, headers=None, body=None, req_url=None, real_url=None,
                 msg='OK', id=None, time=0.2, charset=None):
        self._code = status_code
        self._headers = headers
        self._req_url = req_url
        self._real_url = real_url
        self._body = body
        self._raw_body = body
        self._msg = msg
        self._time = time
        self._charset = charset
        # Response对象唯一标示属性
        self.id = id if id else uuid.uuid1()

    def __contains__(self, string_to_test):
        return string_to_test in self.body

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_code(self, code):
        self._code = code

    def get_code(self):
        return self._code

    def set_url(self, url):
        self._req_url = url

    def get_url(self):
        return self._req_url

    def set_body(self, body):
        self._body = body

    def get_body(self):
        return self._body

    def get_cookies(self):
        if "set-cookie" in self._headers.keys():
            return self._headers["set-cookie"]
        else:
            return None

    def get_headers(self):
        return self._headers

    @property
    def url(self):
        return self._real_url

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        if self._code is None:
            return self._body
        if self._body is None:
            self._body, self._charset = self._charset_handling()
        return self._body

    @property
    def charset(self):
        if self._code is None:
            return self._charset
        if self._charset is None:
            self._body, self._charset = self._charset_handling()
        return self._charset

    def set_charset(self, charset):
        self._charset = charset

    def get_charset(self):
        return self._charset

    def get_status_line(self):
        return 'HTTP/1.1' + SP + str(self._code) + SP + CRLF

    def get_lowercase_headers(self):
        return dict((k.lower(), v) for k, v in self._headers.items())

    def _charset_handling(self):
        lowercase_headers = self.get_lowercase_headers()
        charset = self._charset
        rawbody = self._raw_body
        if charset != DEFAULT_CHARSET and lowercase_headers.get('content-type'):
            charset_mo = re.search('charset=\s*?([\w-]+)', lowercase_headers['content-type'])
            if charset_mo:
                charset = charset_mo.groups()[0].lower().strip()
            else:
                charset_mo = re.search('<meta.*?content=".*?charset=\s*?([\w-]+)".*?>', rawbody, re.IGNORECASE)
                if charset_mo:
                    charset = charset_mo.groups()[0].lower().strip()
                else:
                    try:
                        raise Exception
                    except:
                        charset = DEFAULT_CHARSET
            try:
                _body = str(rawbody)
            except:
                charset = "gbk"
                try:
                    _body = bytes(rawbody, charset)
                except UnicodeDecodeError as e:
                    _body = rawbody
                    charset = "UNKNOWN"
        else:
            _body = str(rawbody, "utf-8")
        return _body, charset

    def __str__(self):
        return_string = "HTTP/1.1 " + str(self._code) + ' ' + self._msg + '\r\n'
        if self.headers:
            return_string += CRLF.join(h + ':' + hv for h, hv in self.headers.items()) + CRLF
        if self.body:
            return_string += CRLF + self.body.decode("utf-8")
        return return_string

    def __repr__(self):
        vals = {'code': self.get_code(), 'url': str(self.get_url()), 'id': self.id}
        return "<Response | %(code)s | %(url)s | %(id)s>" % vals


if __name__ == '__main__':
    url = "http://www.baidu.com"
    res = requests.get(url)
    response = from_requests_response(res, url)

    print("id: ", response.get_id())
    print("url: ", response.get_url())
    print("headers: ", response.get_headers())
    print("cookies: ", response.get_cookies())
    print("code: ", response.get_code())
    print("charset: ", response.get_charset())
    print("lowdercase_headers: ", response.get_lowercase_headers())
    print("status_line: ", response.get_status_line())
    print("body: ", response.get_body())