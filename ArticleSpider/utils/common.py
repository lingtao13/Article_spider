# _*_ coding:utf-8 _*_
import hashlib

import re

__author__ = 'nelson'
__date__ = '2018/4/10 下午2:08'

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

if __name__ == "__main__":
    print (get_md5("http://jobbole.com".encode("utf-8")))

