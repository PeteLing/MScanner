# coding=utf-8
import copy
from web.http.function import is_similar_url


url_list = [
    "http://www.anquanbao.com",
    "http://www.anquanbao.com/index.php",
    "http://www.anquanbao.com/index.php?a=1",
    "http://www.anquanbao.com/index.php?a=6",
    "http://www.anquanbao.com/index.php?b=10",
    "http://www.anquanbao.com/index.php?b=test",
    "http://www.anquanbao.com/index.php?a=1&b=1"
]
# url_list = [
#     "http://www.anquanbao.com/index.php?a=1",
#     "http://www.anquanbao.com/index.php?a=6",
#     "http://www.anquanbao.com/index.php?b=6",
#     "http://www.anquanbao.com/index.php?b=10"
# ]

result = []

temp_list = copy.deepcopy(url_list)
if len(temp_list) > 1:
    result.append(temp_list[0])
    del temp_list[0]
    for a in temp_list:
        flag = False
        for b in result:
            if not is_similar_url(a, b):
                flag = True
            else:
                flag = False
                break
        if flag:
            result.append(a)

print("去似去含前的数据：")
print(url_list)
print("去似去含后的数据：")
print(result)
