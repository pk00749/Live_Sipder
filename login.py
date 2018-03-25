import urllib.request
from selenium import webdriver
import time
import os

def start_chrome():
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(30)  # 隐式等待
    return driver

def open_url():
    # driver = webdriver.PhantomJS()
    # driver.get("http://hotel.qunar.com/")
    driver = start_chrome()
    url="http://www.huya.com/a16789"
    driver.get(url)
    driver.implicitly_wait(15)
    data = driver.title
    print(data)

    return driver


def send_msg():
    driver = open_url()
    driver.find_element_by_link_text("登录").click()
    driver.implicitly_wait(15)
    frame = driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
    driver.switch_to.frame(frame)
    time.sleep(3)
    ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
    ele.send_keys("13250219510")

    ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
    ele.send_keys("81302137hy")

    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()
    print("Login success")
    time.sleep(5)
    driver.switch_to.default_content() # switch to main page
    msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")
    msg.send_keys('Hello')
    time.sleep(3)
    # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
    driver.find_element_by_id('msg_send_bt').click()
    time.sleep(3)
    msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")


if __name__ == '__main__':
    send_msg()