# coding=utf-8

import sys
import urllib
import re
import traceback
import urllib.parse

from lxml import etree
from web.http.URL import URL
from web.http.Request import Request
from web.http.encode_decode import htmldecode
from web.util.smart_fill import smart_fill
from web.http.postdata import postdata as postdata

from wCurl import wcurl
from LogManager import log as om

DEFAULT_ENCODING = "utf-8"


class HtmlParser:

    URL_HEADERS = ('location', )
    URL_TAGS = ('a', 'img', 'link', 'script', 'iframe', 'object', 'embed', 'area', 'frame', 'applet', 'input', 'base',
                "div", 'layer', 'form')
    URL_ATTRS = ('href', 'src', 'data', 'action')
    URL_RE = re.compile('((http|https)://([\w:@\-\./]*?)[^ \n\r\t"\'<>)\s]*)', re.U)
    SAFE_CHARS = (('\x00', '%00'), )

    def __init__(self, response):
        self._encoding = DEFAULT_ENCODING
        self._base_url = response.get_url()

        # Internal state variables
        self._inside_form = False
        self._inside_select = False
        self._inside_textarea = False
        self._inside_script = False

        # Internal containers
        self._tag_and_url = set()
        self._parsed_urls = set()

        self._g_urls = set()
        self._p_urls = set()

        self._forms = []
        self._comments_in_doc = []
        self._scripts_in_doc = []
        self._meta_redirs = []
        self._meta_tags = []

        # To store results
        self._emails = []
        self._form_reqs = []
        self._re_urls = set()
        self._tag_urls = set()

        # Do some stuff before actually parsing
        self._pre_parse(response)

        # Parse
        self._parse(response)

    def start(self, tag, attrs):

        # Called by the parser on element open.
        try:
            meth = getattr(self, '_handle_' + tag + '_tag_start', lambda *args: None)

            meth(tag, attrs)

            if tag.lower() in self.URL_TAGS:
                self._find_tag_urls(tag, attrs)

        except Exception as ex:
            msg = 'An exception occurred while parsing a document: %s' % ex
            om.error(msg)
            om.error('Error traceback: %s' % traceback.format_exc())

    def end(self, tag):

        # Called by the parser element close
        getattr(self, '_handle_' + tag + '_tag_end', lambda arg: None)(tag)

    def close(self):
        pass

    # 获取响应头中的URL
    def _find_header_urls(self, headers):
        for key, value in headers.items():
            if key in self.URL_HEADERS:
                if value.startswith('http'):
                    u = URL(value, encoding=self._encoding)
                else:
                    u = self._base_url.urljoin(value).url_string
                    u = URL(u, encoding=self._encoding)
                # print(url)
                self._tag_urls.add(u)

    # 获取内容标签中的URL
    def _find_tag_urls(self, tag, attrs):
        for attr_name, attr_value in attrs.items():
            if attr_name in self.URL_ATTRS and attr_value and not attr_value.startswith('#'):
                try:
                    if attr_value.startswith("http"):
                        u = URL(attr_value, encoding=self._encoding)
                    else:
                        u = self._base_url.urljoin(attr_value).url_string
                        u = URL(u, encoding=self._encoding)
                except ValueError:
                    pass
                else:
                    self._tag_urls.add(u)

    # 获取满足URL形式的数据
    def _regex_url_parse(self, doc_str):

        if type(doc_str) is bytes:
            doc_str = doc_str.decode('utf-8')
        re_urls = set()
        for url in re.findall(HtmlParser.URL_RE, doc_str):
            try:
                url = URL(url[0], encoding=self._encoding)
            except ValueError:
                pass
            else:
                re_urls.add(url)

        def find_relative(doc_str):
            res = set()
            # 形如index.php 或 index.php?aid=1&bid=2的相对URL
            regex = '([/]{0,1}\w+\.(asp|html|php|jsp|aspx|htm)(\?([\w%]*=[\w%]*)(&([\w%]*=[\w%]*))*){0,1})'
            relative_regex = re.compile(regex, re.U | re.I)
            for match_tuple in relative_regex.findall(doc_str):
                match_str = match_tuple[0]
                url = self._base_url.urljoin(match_str).url_string
                url = URL(url, encoding=self._encoding)
                res.add(url)
            return res

        re_urls.update(find_relative(doc_str))
        self._re_urls.update(re_urls)

    def _decode_URL(self, url_string):
        enc = self._encoding
        is_str = False
        if isinstance(url_string, str):
            is_str = True
            url_string = url_string.encode(enc)
        dec_url = urllib.parse.unquote(url_string)
        for sch, repl in self.SAFE_CHARS:
            dec_url = dec_url.replace(sch, repl)
        if is_str:
            dec_url = dec_url.decode(enc, 'ignore')
        return dec_url

    def _pre_parse(self, response):
        dict_headers = response.headers
        str_headers = ""
        for key, val in dict_headers.items():
            str_headers += key + ':' + val + "\r\n"
        self._regex_url_parse(str_headers)
        self._find_header_urls(dict_headers)
        self._regex_url_parse(response.body)

    def _parse(self, response):
        parser = etree.HTMLParser(target=self, recover=True)
        try:
            etree.fromstring(response.body, parser)
        except ValueError:
            pass

    @property
    def forms(self):
        return self._forms

    def get_forms(self):
        return self.forms

    @property
    def urls(self):
        return self._re_urls, self._tag_urls

    def get_get_urls(self):
        return self._re_urls, self._tag_urls

    def get_form_reqs(self):
        return self._form_reqs

    def _handle_form_tag_start(self, tag, attrs):
        self._inside_form = True
        method = attrs.get('method', 'POST')
        name = attrs.get('name', '')
        action = attrs.get('action', None)

        missing_or_invalid_action = action is None
        if not missing_or_invalid_action:
            try:
                action = self._base_url.urljoin(action)
            except ValueError:
                missing_or_invalid_action = True

        if missing_or_invalid_action:
            action = self._base_url

        form_data = postdata(encoding=self._encoding)
        form_data.set_name(name)
        form_data.set_method(method)
        form_data.set_action(action)

        self._forms.append(form_data)

    def _handle_form_tag_end(self, tag):
        self._inside_form = False
        form_data = self._forms[-1]
        url = form_data.get_action()
        method = form_data.get_method()
        freq = Request(url)
        freq.set_method(method)
        freq.set_post_data(form_data)

        self._form_reqs.append(freq)

    def _handle_input_tag_start(self, tag, attrs):
        side = 'inside' if self._inside_form else 'outside'
        default = lambda *args: None
        meth = getattr(self, '_handle_' + tag + '_tag_' + side + '_form', default)
        meth(tag, attrs)

    def _handle_input_tag_inside_form(self, tag, attrs):
        form_data = self._forms[-1]
        type = attrs.get('type', '').lower()
        name = attrs.get('name', '')
        value = attrs.get('value', '')
        items = attrs.items()
        if name == '':
            return
        if value == '':
            value = smart_fill(name)
        if type == 'file':
            form_data.hasFileInput = True
        else:
            form_data.set_data(name, value)


if __name__ == '__main__':
    url = "http://www.goctf.cn/"
    r = wcurl.get(url, allow_redirects=False)
    parser = HtmlParser(r)
    print(r)
    re_url, parser_url = parser.urls
    print("Parser URL:")
    for item in parser_url:
        print(item)
    print("Regex URL:")
    for item in re_url:
        print(item)

    a = parser.get_form_reqs()
    if len(a) > 0:
        print(a[0])
