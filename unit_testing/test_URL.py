# coding=utf-8

from web.http.URL import URL


def TestURL():
    url = URL("http://www.anquanbao.com/book/index.php?id=1#top")
    assert url.get_host() == "www.anquanbao.com"
    assert url.get_port() == 80
    assert url.get_path() == "/book/index.php"
    assert url.get_filename() == "index.php"
    assert url.get_ext() == "php"
    assert url.get_query() == "id=1"
    assert url.get_fragment() == "top"
    print(url.url_string)
    print(url)


if __name__ == '__main__':
    TestURL()