# _*_ coding:utf-8 _*_
__author__ = 'nelson'
__date__ = '2018/4/13 下午12:09'

import requests
from http.cookiejar import LWPCookieJar
import hmac
from hashlib import sha1
import re
import json
import time
import base64
from PIL import Image
from lxml import etree

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive'
}

session = requests.session()
session.cookies = LWPCookieJar(filename='cookie.json')

LOGIN = 'https://www.zhihu.com/signup'
POST = 'https://www.zhihu.com/api/v3/oauth/sign_in'

FORM_DATA = {
    "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
    "grant_type": "password",
    "source": "com.zhihu.web",
    "lang": "en",
    "ref_source": "homepage"
}


def get_captcha(headers):
    response = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    r = re.findall('"show_captcha":(\w+)', response.text)
    if r[0] == 'false':
        return ''
    else:
        response = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
        show_captcha = json.loads(response.text)['img_base64']
        with open('captcha.jpg', 'wb') as f:
            f.write(base64.b64decode(show_captcha))
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input('输入验证码:')
        session.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers,
                     data={"input_text": captcha})
        return captcha


# udid的值是cookie中d_c0的值"AOAgaM4QaQ2PTlEjjfm2eSr2NHEKHpK2q9o=|1523169135"  注意是竖线前部分AOAgaM4QaQ2PTlEjjfm2eSr2NHEKHpK2q9o=
# 亲测：头信息可以不带udid
def get_xsfr():
    response = session.get(LOGIN, headers=HEADERS)
    cookie = response.cookies.get_dict()
    xsrf = cookie.get('_xsrf', False)
    if not xsrf:
        get_xsfr
    else:
        return xsrf


def get_sign(t):
    h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    now = t
    h.update((grant_type + client_id + source + now).encode('utf-8'))
    return h.hexdigest()


def login(username=None, password=None):
    if not username:
        username = input('请输入手机号:')
    if not password:
        password = input('请输入密码')
    username = '+86' + username
    headers = HEADERS.copy()
    xsrf = get_xsfr()
    headers.update({
        # "X-UDID":udid,
        "X-Xsrftoken": xsrf,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    })
    t = str(int((time.time() * 1000)))
    form_data = FORM_DATA.copy()
    form_data.update({
        'username': username,
        'password': password,
        'captcha': get_captcha(headers),
        'timestamp': t,
        'signature': get_sign(t)
    })
    response = session.post(POST, data=form_data, headers=headers)
    if response.status_code == 201:
        print('登陆成功，你可以查看cookie.json中的cookie信息')
        session.cookies.save()

def is_login():
    # 通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/people/nelson-peng/activities"
    response = session.get(inbox_url, headers=HEADERS, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


if __name__ == '__main__':
    try:
        session.cookies.load(ignore_discard=True)
        response = session.get('https://www.zhihu.com/', headers=HEADERS)
        htmls = response.content.decode('utf-8')
        selector = etree.HTML(htmls)
        for x in selector.xpath('//div[@class="Card TopstoryItem TopstoryItem--experimentExpand"]'):
            print(x.xpath('.//a[@data-za-detail-view-element_name="Title"]/text()'))

    except:
        login()
        response = session.get('https://www.zhihu.com/', headers=HEADERS)
        response.content.decode('utf-8')
