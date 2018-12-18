# _*_ coding:utf-8 _*_
__author__ = 'nelson'
__date__ = '2018/4/12 下午10:01'

from selenium import webdriver
from scrapy.selector import Selector

browser=webdriver.Chrome(executable_path="/Users/nelsonpeng/PycharmProjects/ArticleSpider/chromedriver")

browser.get("https://www.zhihu.com/signin")

browser.find_element_by_css_selector(".SignFlow input[name='username']").send_keys("13590371957")
browser.find_element_by_css_selector(".SignFlow input[name='password']").send_keys("140140")

browser.find_element_by_css_selector(".SignFlow button.SignFlow-submitButton").click()
# browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()


# print(browser.page_source)

# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tb-promo-price .tb-rmb-num::text").extract())