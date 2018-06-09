import queue
from selenium import webdriver
import threading
import time, json, os, pickle
import pymongo
from logging import getLogger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'huya',
    'user_name': None,
    'password': None
}

class conphantomjs:
    jiange = 0.00001  ##开启phantomjs间隔
    timeout = 20  ##设置phantomjs超时时间
    # path = "D:\python27\Scripts\phantomjs.exe"  ##phantomjs路径
    # service_args = ['--load-images=no', '--disk-cache=yes']  ##参数设置

    def __init__(self, name):
        self.logger = getLogger(__name__)
        self.phantomjs_max = 5  ##同时开启phantomjs个数
        self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
        self.db = self.conn[MONGODB_CONFIG['db_name']]
        self.q_phantomjs = queue.Queue()  ##存放phantomjs进程队列
        self.user_name = name

    def login(self, d):
        self.logger.info('logging...')
        # popup = browser.switch_to_frame('udb_exchange3lgn')
        WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.ID, 'nav-login'))).click()
        WebDriverWait(d, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='udbsdk_frm_normal']")))
        time.sleep(1)
        ele = d.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys('13250219510')

        ele = d.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys('81302137hy')

        time.sleep(1)
        d.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()

        time.sleep(1)

    def saveCookies(self, driver, name):
        self.logger.info('saving cookies...')
        pickle.dump(driver.get_cookies(), open("{user_name}.pkl".format(user_name=name), "wb"))

    def load_cookie(self, n, name):
        self.logger.info('loading cookies...')
        for i in range(1, len(n)):
            if n[i]['name'] == name:
                print(n[i]['value'])
                return n[i]['value']

    def addCookiesWithURL(self, browser, name):
        print('adding cookies...')
        try:
            with open('{user_name}.pkl'.format(user_name=name), 'rb')as fp:
                n = pickle.load(fp)
                # browser.add_cookie({'name': 'Hm_lvt_51700b6c722f5bb4cf39906a596ea41f',
                #                     'value': self.load_cookie(n, 'Hm_lvt_51700b6c722f5bb4cf39906a596ea41f')})  #
                # browser.add_cookie({'name': 'h_pr', 'value': self.load_cookie(n, 'h_pr')})  #
                # browser.add_cookie({'name': 'udb_passdata', 'value': self.load_cookie(n, 'udb_passdata')})
                # browser.add_cookie({'name': 'yyuid', 'value': self.load_cookie(n, 'yyuid')})  #
                # browser.add_cookie({'name': '__yaoldyyuid', 'value': self.load_cookie(n, '__yaoldyyuid')})  #
                # browser.add_cookie({'name': 'username', 'value': self.load_cookie(n, 'username')})  #
                # browser.add_cookie({'name': 'password', 'value': self.load_cookie(n, 'password')})  #
                # browser.add_cookie({'name': 'udboauthtmptokensec', 'value': self.load_cookie(n, 'udboauthtmptokensec')})
                # browser.add_cookie({'name': 'osinfo', 'value': self.load_cookie(n, 'osinfo')})  #
                # browser.add_cookie({'name': 'udb_l',
                #                     # 'value': 'DAAyMjMyNjg0MTI4eXl-PBtbAnQAkYmSqZyuZg_t9LxMgLv3nP00wp6101IPZpC9rfnmYQVoW5K3OQQOL69sXjX1EGBzQm51qJGolwy8gUmgDKwxIzWFe3hyKT7m_Xs71bPBD7X91iirBqjb2o73iXzrCQ1l2PGLpfbutXNDaDC0FqAlKaV-ljUAAAAAAwAAAAAAAAAMADExMy42NS43MS4zNAQANTIxNg=='})
                #                     'value': self.load_cookie(n, 'udb_l')})
                # browser.add_cookie({'name': 'udb_n',
                #                     # 'value': '4ae860d58b80bbdd1172e9aacfe6684c9c8302a673ccdd476faa34342e4353f2fad9c23d3ebb792ebba724367a94ab97'})
                #                     'value': self.load_cookie(n, 'udb_n')})
                # browser.add_cookie({'name': 'udb_c',
                #                     # 'value': 'AECPJFBqAAJgADqaaNumrKXZuokRvAcJibvzmARlj2W_ytgnKJ8ma3dlpmhlPaCCgBmOhk6K13qL61dHdMs7qd_2H2pa7EgO8qR1PfR9HE2kXPaEL6tMHFWxClvXcS5ZbX5JLIvV04yOiw=='})
                #                     'value': self.load_cookie(n, 'udb_c')})
                # browser.add_cookie({'name': 'udb_oar',
                #                     # 'value': '8FF226293125A2FDEB10694D410C7D895FE29F051908ADDACF1422A84BB36D9932681C2AA49FDB0C6EF11D8068E168C5D823BB7D7466B61FFF3E757E6BB2947AB1BBB4DD8D969467B0DEE410CDD2CE25B885B8263D8FD3E484992B9F5003E01C14A41E30B8E29C95BD72B50269543E89E73DAE963AF14585522A23B37392B65E349039C99625896DBC198045DDE7CE4D26652A21CA69BB07CFFD78522284E577E3BF5463370DFFA8935B97AE67A357A6DDB9BF9885A1037BF3FE284EF1154B80B0AED4771002AFCD8C363DCE7B580CCE6C984888BB2238DA6B13804D404E19FF68DB0FA92CEDEB4970E69005E96CB1A33CC300AD6681852064A96C48E55FF9CF12F68479A3A89064CA082364FBB6D849930BA0E2548D62AA4E38D385A89FB58A62F959F818A207462987AF99FD0617C3BFF85FF6145D61A653DE1466161496C5'})
                #                     'value': self.load_cookie(n, 'udb_oar')})
                # browser.add_cookie({'name': 'Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f',
                #                     'value': self.load_cookie(n, 'Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f')})  #
                # browser.add_cookie({'name': '_yasids', 'value': self.load_cookie(n, '_yasids')})  #
                # browser.add_cookie({'name': 'udboauthtmptoken',
                #                     # 'value': '899b691864c88d8397525861193f70222b816b28ea3b9dc3b39979cac6072382aa703eb5bbcaa5d4bce15fd6c934553a'})
                #                     'value': self.load_cookie(n, 'udboauthtmptoken')})
                # browser.add_cookie({'name': 'PHPSESSID', 'value': self.load_cookie(n, 'PHPSESSID')})  #
                # browser.add_cookie({'name': '__yamid_tt1', 'value': self.load_cookie(n, '__yamid_tt1')})  #
                # browser.add_cookie({'name': '__yamid_new', 'value': self.load_cookie(n, '__yamid_new')})  #
                # browser.add_cookie({'name': '__yasmid', 'value': self.load_cookie(n, '__yasmid')})  #
                # browser.add_cookie({'name': 'h_unt', 'value': self.load_cookie(n, 'h_unt')})  #

                browser.add_cookie({'name': 'Hm_lvt_51700b6c722f5bb4cf39906a596ea41f', 'value': '1528511556'})  #
                browser.add_cookie({'name': 'h_pr', 'value': '1'})  #
                browser.add_cookie({'name': 'udb_passdata', 'value': '1'})
                browser.add_cookie({'name': 'yyuid', 'value': '2232479408'})  #
                browser.add_cookie({'name': '__yaoldyyuid', 'value': '2232479408'})  #
                browser.add_cookie({'name': 'username', 'value': '2232684128yy'})  #
                browser.add_cookie({'name': 'password', 'value': '3052411AD09E88D82E9D718C350BE0D0EEED51FC'})  #
                browser.add_cookie({'name': 'udboauthtmptokensec', 'value': ''})
                browser.add_cookie({'name': 'osinfo', 'value': '5DA8C4FC5A761006EC0B212DA59D5686F21BFCD4'})  #
                browser.add_cookie({'name': 'udb_l',
                                    'value': 'DAAyMjMyNjg0MTI4eXl-PBtbAnQAkYmSqZyuZg_t9LxMgLv3nP00wp6101IPZpC9rfnmYQVoW5K3OQQOL69sXjX1EGBzQm51qJGolwy8gUmgDKwxIzWFe3hyKT7m_Xs71bPBD7X91iirBqjb2o73iXzrCQ1l2PGLpfbutXNDaDC0FqAlKaV-ljUAAAAAAwAAAAAAAAAMADExMy42NS43MS4zNAQANTIxNg=='})
                # 'value': load_cookie(n, 'udb_l')})
                browser.add_cookie({'name': 'udb_n',
                                    'value': '4ae860d58b80bbdd1172e9aacfe6684c9c8302a673ccdd476faa34342e4353f2fad9c23d3ebb792ebba724367a94ab97'})
                # 'value': load_cookie(n, 'udb_n')})
                browser.add_cookie({'name': 'udb_c',
                                    'value': 'AECPJFBqAAJgADqaaNumrKXZuokRvAcJibvzmARlj2W_ytgnKJ8ma3dlpmhlPaCCgBmOhk6K13qL61dHdMs7qd_2H2pa7EgO8qR1PfR9HE2kXPaEL6tMHFWxClvXcS5ZbX5JLIvV04yOiw=='})
                # 'value': load_cookie(n, 'udb_c')})
                browser.add_cookie({'name': 'udb_oar',
                                    'value': '8FF226293125A2FDEB10694D410C7D895FE29F051908ADDACF1422A84BB36D9932681C2AA49FDB0C6EF11D8068E168C5D823BB7D7466B61FFF3E757E6BB2947AB1BBB4DD8D969467B0DEE410CDD2CE25B885B8263D8FD3E484992B9F5003E01C14A41E30B8E29C95BD72B50269543E89E73DAE963AF14585522A23B37392B65E349039C99625896DBC198045DDE7CE4D26652A21CA69BB07CFFD78522284E577E3BF5463370DFFA8935B97AE67A357A6DDB9BF9885A1037BF3FE284EF1154B80B0AED4771002AFCD8C363DCE7B580CCE6C984888BB2238DA6B13804D404E19FF68DB0FA92CEDEB4970E69005E96CB1A33CC300AD6681852064A96C48E55FF9CF12F68479A3A89064CA082364FBB6D849930BA0E2548D62AA4E38D385A89FB58A62F959F818A207462987AF99FD0617C3BFF85FF6145D61A653DE1466161496C5'})
                # 'value': load_cookie(n,'udb_oar')})
                browser.add_cookie({'name': 'Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f', 'value': '1528511560'})  #
                browser.add_cookie({'name': '_yasids', 'value': '__rootsid%3DC804B111E9C000016C6BB7CD1FA011CF'})  #
                browser.add_cookie({'name': 'udboauthtmptoken',
                                    'value': '899b691864c88d8397525861193f70222b816b28ea3b9dc3b39979cac6072382aa703eb5bbcaa5d4bce15fd6c934553a'})
                # 'value': load_cookie(n, 'udboauthtmptoken')})
                browser.add_cookie({'name': 'PHPSESSID', 'value': 'un4jcirn926k4ej7819atg4ih5'})  #
                browser.add_cookie({'name': '__yamid_tt1', 'value': '0.20169332498077597'})  #
                browser.add_cookie({'name': '__yamid_new', 'value': 'C804B110B56000014141B3D3157E1BCB'})  #
                browser.add_cookie({'name': '__yasmid', 'value': '0.20169332498077597'})  #
                # browser.add_cookie({'name': 'h_unt', 'value': load_cookie(n, 'h_unt')})  #
        except EOFError:  # 捕获异常EOFError 后返回None
            print('EOFError')

    def access(self):
        chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        option = webdriver.ChromeOptions()
        # option.add_argument('headless') # can't use
        driver = webdriver.Chrome(chromedriver, chrome_options=option)
        driver.maximize_window()
        driver.get("https://www.huya.com/g")
        self.login(driver)
        self.saveCookies(driver, self.user_name)

    def accessWithCookie(self, driver, url):
        driver.maximize_window()
        driver.get(url)
        time.sleep(0.5)
        self.addCookiesWithURL(driver, self.user_name)
        time.sleep(0.5)
        driver.refresh()

        self.saveCookies(driver, self.user_name)

    def getbody(self, url):
        '''利用phantomjs获取网站源码以及url'''
        d = self.q_phantomjs.get()
        print(d)
        try:
            if os.path.exists('{user_name}.pkl'.format(user_name=self.user_name)):
                self.logger.info('cookie found...')
                self.accessWithCookie(d, url)
            time.sleep(1)
        except:
            print("Phantomjs Open url Error")

        self.send_msg(d, '666')
        url = d.current_url
        self.q_phantomjs.put(d)
        print(url)

    def open_phantomjs(self):
        '''多线程开启phantomjs进程'''
        def open_threading():
            # service_args = []
            # service_args.append('--disk-cache=yes')
            # service_args.append('--ignore-ssl-errors=true')
            # driver = webdriver.PhantomJS() # service_args=service_args # service_args.append('--load-image=no')
            # d = webdriver.PhantomJS(service_args=service_args)  # service_args=conphantomjs.service_args
            # d.implicitly_wait(conphantomjs.timeout)  ##设置超时时间
            # d.set_page_load_timeout(conphantomjs.timeout)  ##设置超时时间
            # d.maximize_window()

            chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            option = webdriver.ChromeOptions()
            # option.add_argument('headless') # can't use
            d = webdriver.Chrome(chromedriver, chrome_options=option)

            self.q_phantomjs.put(d)  # 将phantomjs进程存入队列

        th = []
        for i in range(self.phantomjs_max):
            t = threading.Thread(target=open_threading)
            th.append(t)
        for i in th:
            i.start()
            time.sleep(conphantomjs.jiange)  # 设置开启的时间间隔
        for i in th:
            i.join()

    def close_phantomjs(self):
        '''多线程关闭phantomjs对象'''
        th = []

        def close_threading():
            d = self.q_phantomjs.get()
            d.quit()

        for i in range(self.q_phantomjs.qsize()):
            t = threading.Thread(target=close_threading)
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()

    def main(self):
        # 1. check cookies exist or not. if not, give cookies
        if not os.path.exists('{user_name}.pkl'.format(user_name=self.user_name)):
            self.access()

        # 2. run open_phantomjs, create the process of phantomjs
        self.phantomjs_max = 1
        self.open_phantomjs()
        print("phantomjs num is ", self.q_phantomjs.qsize())

        urls = []
        count = self.db['rooms'].count()
        for e in range(0, count // 10 + 1):
            # print('---------------%d' % e)
            res = self.db['rooms'].find({'_id': {'$gte': 10 * e, '$lt': 10 * (e + 1)}})
            for k in res:
                urls.append(k['room'])
            # print(urls)
            # print('---------------')
            # urls = ["http://www.baidu.com"] * 50
            th = []
            for i in urls:
                i = 'https://www.huya.com/' + i
                t = threading.Thread(target=cur.getbody, args=(i,))
                th.append(t)
            for i in th:
                i.start()
            for i in th:
                i.join()
            urls = []

        self.close_phantomjs()
        print("phantomjs num is ", self.q_phantomjs.qsize())

# https://lgn.yy.com/lgn/oauth/authorize.do?oauth_token=b7e2debe51603ff22075819a5ca17e828810b7de69530da6d59a35a5cb78b5139b85cd08af12b31ec50608b67fa24628&denyCallbackURL=&regCallbackURL=https://www.huya.com/udb_web/udbport2.php?do=callback&UIStyle=xelogin&rdm=0.14674353878945112

    # def is_login(self, driver, room_url):
    #     # login_name = driver.find_element_by_xpath("//*[@id='login-username']").text
    #     # print(response.xpath('//span[@id="login-username"]/@title').extract()[0])
    #     if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "": #//*[@id="login-username"]
    #         print('Need to login')
            # self.login()
            # self.save_cookie()
        # else:
        #     print("NO need to login")
        # driver.get(room_url)
        # self.send_advertisement(driver)


    def send_msg(self, driver, msg):
        msg_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pub_msg_input']")))
    #     msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg_input.send_keys(msg)
        # time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'msg_send_bt'))).click()
        # d.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        # self.driver.find_element_by_id('msg_send_bt').click()
        time.sleep(1)
        print('Message 1 sent!')



if __name__ == "__main__":
    cur = conphantomjs('13250219510')
    cur.main()

    # with open('{user_name}.json'.format(user_name=__username), 'r', encoding='utf-8') as f:
        #         listCookies = json.loads(f.read())
        #     for cookie in listCookies:
        #         d.add_cookie({
        #             'domain': '.huya.com',  # 此处xxx.com前，需要带点
        #             'name': cookie['name'],
        #             'value': cookie['value'],
        #             'path': '/',
        #             'expires': None,
        #             'httpOnly': False,
        #             'secure': False
        #         })
        # d.get(url, cookies=)
        # -----------------------------------------------------------------
        # msg_input = WebDriverWait(d, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[@id='pub_msg_input']")))
        #     msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        # msg_input.send_keys('6666')
        # time.sleep(2)
        # WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.ID, 'msg_send_bt'))).click()
        # d.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        # self.driver.find_element_by_id('msg_send_bt').click()
        # time.sleep(1)
        # print('Message 1 sent!')

    '''
        用法：
        1.实例化类
        2.运行open_phantomjs 开启phantomjs进程
        3.运行getbody函数，传入url
        4.运行close_phantomjs 关闭phantomjs进程
        '''
    # cur = conphantomjs()
    # conphantomjs.phantomjs_max = 10
    # cur.open_phantomjs()
    # print("phantomjs num is ", cur.q_phantomjs.qsize())
    #
    # urls = []
    # count = cur.db['rooms'].count()
    # for e in range(0, count // 10 + 1):
    #     print('---------------%d' % e)
    #     res = cur.db['rooms'].find({'_id': {'$gte': 10 * e, '$lt': 10 * (e + 1)}})
    #     for k in res:
    #         urls.append(k['room'])
    #     print(urls)
    #     print('---------------')
    # urls = ["http://www.baidu.com"] * 50
    #     th = []
    #     for i in urls:
    #         i = 'https://www.huya.com/' + i
    #         t = threading.Thread(target=cur.getbody, args=(i,))
    #         th.append(t)
    #     for i in th:
    #         i.start()
    #     for i in th:
    #         i.join()
    #     urls = []
    #
    # cur.close_phantomjs()
    # print("phantomjs num is ", cur.q_phantomjs.qsize())

    # url_list = ["http://www.baidu.com"] * 50
    # th = []
    # for i in url_list:
    #     t = threading.Thread(target=cur.getbody, args=(i,))
    #     th.append(t)
    # for i in th:
    #     i.start()
    # for i in th:
    #     i.join()
    # cur.close_phantomjs()
    # print("phantomjs num is ", cur.q_phantomjs.qsize())
