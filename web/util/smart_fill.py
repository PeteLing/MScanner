# coding=utf-8

from LogManager import log


form_name_kb = {
    'scanner': ['username', 'user', 'userid', 'nickname', 'name'],
    'abc123456': ['password', 'pass', 'pwd'],
    'test@watscan.com': ['email', 'mail', 'usermail'],
    '12380000': ['mobile'],
    'this is just for a test': ['content', 'text', 'query', 'search', 'data', 'comment'],
    'www.test.com': ['domain'],
    'http://www.test.com': ['link', 'url', 'website']
}


def smart_fill(variable_name):
    variable_name = variable_name.lower()
    flag = False
    for filled_value, variable_name_list in form_name_kb.items():
        for variable_name_db in variable_name_list:
            if variable_name_db == variable_name:
                flag = True
                return filled_value
    if not flag:
        msg = '[smart_fill Failed to find a value for parameter with name "]'
        msg += variable_name + '".'
        log.debug(msg)
        return 'UNKNOWN'


if __name__ == '__main__':
    print("username=%s" % smart_fill("username"))
    print("password=%s" % smart_fill("password"))
    print("domain=%s" % smart_fill("domain"))
    print("email=%s" % smart_fill("email"))
    print("content=%s" % smart_fill("content"))
