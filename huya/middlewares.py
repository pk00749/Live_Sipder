# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random, time, pickle
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from logging import getLogger


class HuyaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        print("process_spider_input")
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        print("process_spider_output")
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    # def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        # print("process_spider_exception")
        # Should return either None or an iterable of Response, dict
        # or Item objects.
        # pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        print("process_start_requests")
        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class MyCustomDownloaderMiddleware(UserAgentMiddleware):
    # def __init__(self, user_agent=''):
    # super(MyCustomDownloaderMiddleware, self).__init__(user_agent)
class MyCustomDownloaderMiddleware(object):
    def __init__(self, timeout=None): #, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        # self.driver = webdriver.PhantomJS()
        # self.driver.maximize_window()
        # self.driver.set_page_load_timeout(self.timeout)
        # self.wait = WebDriverWait(self.driver, self.timeout)
        # self.pickle = pickle.load(open("./json/temp.pkl", "rb"))

    # def __del__(self):
    #     self.driver.close()

    def process_request(self, request, spider):
        """
                用PhantomJS抓取页面
                :param request: Request对象
                :param spider: Spider对象
                :return: HtmlResponse
        """
        self.logger.debug("Phantomjs is starting")
        __username = '13250219510'  # self.json.get('name')
        __password = '81302137hy'  # self.json.get('password')

        try:
            self.logger.info("Visiting: " + request.url)
            spider.driver.get(request.url)
            # self.driver.get(request.url)
            self.logger.info(spider.driver.title)
            if request.url == 'https://www.huya.com/g/':
            # if spider.driver.find_element_by_xpath("//*[@id='login-username']").text == "":  # //*[@id="login-username"]
                print('Need to login')
                # self.driver.find_element_by_link_text("登录").click()
                WebDriverWait(spider.driver, 10).until(EC.element_to_be_clickable((By.ID, 'nav-login'))).click()
                # self.driver.find_element_by_id('nav-login').click()
                WebDriverWait(spider.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='udbsdk_frm_normal']")))
                # frame = self.driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
                # self.driver.switch_to.frame(frame)
                time.sleep(1)

                ele = spider.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
                ele.send_keys(__username)

                ele = spider.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
                ele.send_keys(__password)

                time.sleep(1)
                spider.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()
                time.sleep(1)
                print("Login success")
                spider.driver.refresh()

                # pickle.dump(spider.driver.get_cookies(),
                #             open("./cookies/{username}.pkl".format(username=self.pickle.get('name')), "wb"))
                return HtmlResponse(url=request.url, body=spider.driver.page_source, request=request, encoding='utf-8', status=200)
            else:
                print("NO need to login")
                return HtmlResponse(url=request.url, body=spider.driver.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

        # else:
            # print(request.url)
            # print(spider.driver.page_source)
            # return HtmlResponse(url=request.url,  request=request, encoding='utf-8', status=200)
        #body=spider.driver.page_source,

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=10)

        # ua = random.choice(self.user_agent_list)
        # if ua:
        #     print(ua)
            # request.headers.setdefault('User-Agent', ua)

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    # user_agent_list = [
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    #     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    #     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    # ]

    # def process_response(self, request, response, spider):
        # Called for each response that goes through the spider middleware and into the spider.
        # find_element_by_xpath("//*[@id='login-username']").text
        # response.xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        # print("process_response")
        # print(response.url)
        # user = response.xpath('//div[@id="nav_login"]').extract()
        # print(user)
        # Should return None or raise an exception.
        # return response
