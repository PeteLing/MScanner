# coding=utf-8

import hashlib


def md5_16(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()[8: -8]


url_list = [
    'http://www.anquanbao.com/1.php',
    'http://www.anquanbao.com/2.php',
    'http://www.anquanbao.com/3.php',
    'http://www.anquanbao.com/1.php'
]

md5_url_dict = {}

result = []

for url in url_list:
    md5_url = md5_16(url)
    md5_url_dict[md5_url] = url

for item in md5_url_dict.keys():
    if item not in result:
       result.append(item)


print("before filter: ", url_list)
print("after filter: ", )
for item in result:
    print(md5_url_dict.get(item))