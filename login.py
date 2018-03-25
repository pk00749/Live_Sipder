import urllib.request
from selenium import webdriver
import time
import os
import pandas as pd
import csv

def start_chrome():
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(30)  # 隐式等待
    return driver


def read_csv():
    # with open('room_list.csv', 'r') as csv_file:
    #     reader = csv.reader(csv_file)
    #     reader.read
    # results = pd.read_csv('room_list.csv')
    # print(results.to_string)
    # print(type(results.to_string))
    all_urls = []
    reader = csv.reader(open('room_list.csv', encoding='utf-8'))
    for url in reader:
        all_urls.append(url[1])

    total_url = len(all_urls)
    return total_url, all_urls


def open_url(url):
    # driver = webdriver.PhantomJS()
    # driver.get("http://hotel.qunar.com/")
    driver = start_chrome()
    # url="http://www.huya.com/a16789"
    driver.get(url)
    driver.implicitly_wait(15)
    data = driver.title
    print(data)

    return driver


def send_msg(url):
    driver = open_url(url)
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


def main():
    total_url, all_urls = read_csv()
    for u in range(1, total_url):
        url = all_urls[u]
        print(url)
        send_msg(url)


if __name__ == '__main__':
    # send_msg()
    main()