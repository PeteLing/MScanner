from web.http.function import is_similar_page
from web.http.Response import from_requests_response

import requests


if __name__ == '__main__':
    url = "http://www.baidu.com"
    res = requests.get(url)
    response = from_requests_response(res, url)

    url2 = "https://blog.csdn.net/madujin/article/details/53152619"
    res2 = requests.get(url2)
    response2 = from_requests_response(res2, url2)

    is_similar_page(response, response2)