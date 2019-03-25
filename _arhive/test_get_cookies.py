# -*- coding:utf-8 -*-

import logging
import logging.config
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, os

# logging.config.fileConfig("logger.conf")

def login(d):
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


def saveCookies(driver):
    print(driver.get_cookies())
    pickle.dump(driver.get_cookies(), open("13250219510.pkl", "wb"))

def load_cookie(n, name):
    for i in range(1, len(n)):
        if n[i]['name'] == name:
            print(n[i]['value'])
            return n[i]['value']

def addCookiesWithURL(browser):
    try:
        with open('186cookies.pkl', 'rb')as fp:
            n = pickle.load(fp)
            browser.add_cookie({'name': 'Hm_lvt_51700b6c722f5bb4cf39906a596ea41f', 'value': '1528511556'}) #
            browser.add_cookie({'name': 'h_pr', 'value': '1'})  #
            browser.add_cookie({'name': 'udb_passdata', 'value': '1'})
            browser.add_cookie({'name': 'yyuid', 'value': '2232479408'})  #
            browser.add_cookie({'name': '__yaoldyyuid', 'value': '2232479408'})  #
            browser.add_cookie({'name': 'username', 'value': load_cookie(n,'username')})  #
            browser.add_cookie({'name': 'password', 'value': load_cookie(n, 'password')})  #
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

def access():
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chromedriver, chrome_options=option)

    driver.maximize_window()
    driver.get("https://www.huya.com/g")
    login(driver)
    saveCookies(driver)

def accessWithCookie():
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chromedriver, chrome_options=option)
    driver.maximize_window()

    driver.get("https://www.huya.com/g")

    print(driver.capabilities['version'])

    time.sleep(1)

    addCookiesWithURL(driver)
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    # driver.get("https://www.huya.com/g")

    print(driver.get_cookies())
    print('--------------------------')
    # pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))
    saveCookies(driver)
    time.sleep(30)

# get cookie
access()

# accessWithCookie()


