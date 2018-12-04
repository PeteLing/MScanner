
from wCurl import wcurl
from web.http.Request import Request


if __name__ == '__main__':
    # res = wcurl.get("http://www.baidu.com")
    # print(res)
    # for i in range(5):
    #     res = wcurl.get('https://freebuf.com')
    #     print(res)
    url = "https://www.freebuf.com"
    req = Request(url)
    response = wcurl._send_req(req)
    print(response.get_body())