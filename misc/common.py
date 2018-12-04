# coding=utf-8

import json
import string
import hashlib
import urllib

from random import choice, randint


def rand_letters(length=0):
    t_list = []
    for i in range(length or randint(6, 10)):
        t_list.append(choice(string.ascii_letters))
    return ''.join(t_list)