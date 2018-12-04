# coding=utf-8


import re
from html.entities import name2codepoint
import urllib.parse
import sys
import urllib


CHAR_REF_PATT = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?', re.U)


def htmldecode(text, use_repr=False):

    def entitydecode(match):
        entity = match.group(1)
        if entity.startswith('#x'):
            return chr(int(entity[2:], 16))
        elif entity.startswith('#'):
            return chr(int(entity[1:]))
        else:
            return match.group(0)

    return CHAR_REF_PATT.sub(entitydecode, text)


# def urlencode(query, encoding, safe='%/\<>"\'=:()'):
#     if hasattr(query, "items"):
#         query = query.items()
#     else:
#         try:
#             if len(query) and not isinstance(query[0], tuple):
#                 raise TypeError
#         except TypeError:
#             try:
#                 tb = sys.exc_info()[2]
#                 raise TypeError
#             finally:
#                 del tb
#     l = []
#     is_unicode = lambda x: isinstance(x, str)
#
#     if encoding == 'gbk':
#         encoding = 'utf-8'
#     for k, v in query:
#         k.encode(encoding) if is_unicode(k) else bytes(k)
#         k = urllib.parse.quote(k, safe)
#         if isinstance(v, str):
#             v = [v]
#         else:
#             try:
#                 len(v)
#             except TypeError:
#                 v = [bytes(v)]
#         for ele in v:
#             ele = ele.encode(encoding) if is_unicode(ele) else bytes(ele)
#             l.append(k + '=' + urllib.parse.quote(ele, safe))
#
#     return '&'.join(l)
def urlencode(query, encoding, safe='%/\<>"\'=:()'):
    return urllib.parse.urlencode(query, encoding=encoding, safe=safe)


if __name__ == '__main__':
    # print(htmldecode(u'hola mundo'))
    # print(htmldecode(u'hólá múndó'))
    # print(htmldecode(u'hola &#0443'))
    # print(htmldecode('hola mundo &#x41'))
    # print(htmldecode('&aacute;'))

    import cgi
    print(urlencode(cgi.parse_qs('a=1&a=c'), 'utf-8'))
    print(urlencode(cgi.parse_qs('a=1&b=c'), 'latin1'))
    print(urlencode(cgi.parse_qs('a=á&a=2'), 'latin1'))
    # print(urlencode(u'a=b&c=d', 'utf-8'))