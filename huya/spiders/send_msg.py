from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, time

from huya.spiders.admin_excel import AdminWorkbook

# chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# driver = webdriver.Chrome(chromedriver, chrome_options=option)
# driver.get('https://www.huya.com/live/552311')
# print('打开浏览器')
# print(driver.title)
# t= driver.find_element_by_id('nav-login')
# print(t)
# print('关闭')
# driver.quit()
# print('测试完成')

# class SEND_MSG:
#     def __init__(self, username, password, no, browser):
#         self.driver = self.start_chrome(browser)
#         self.username = username
#         self.password = password
#         self.excel_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), "huya.xlsx")
#         self.workbook = AdminWorkbook(self.excel_path)
#         self.topic = ''
#         self.no = no
#
#
#     def start_chrome(self, browser):
#         chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
#         os.environ["webdriver.chrome.driver"] = chromedriver
#         option = webdriver.ChromeOptions()
#         # if browser == '-hl':
#         option.add_argument('headless')
#
#         driver = webdriver.Chrome(chromedriver, chrome_options=option)
#         driver.implicitly_wait(30)  # 隐式等待
#         return driver
#
#     def login(self):
#         driver = self.driver
#         __username = self.username
#         __password = self.password
#         title = driver.title
#         print(title)
#
#         # self.driver.find_element_by_link_text("登录").click()
#         # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'nav-login'))).click()
#         # self.driver.find_element_by_id('nav-login').click()
#         t = self.driver.find_element_by_xpath('//*[@id="nav-login"]')
#         t.click()
#
#         # WebDriverWait(driver, 10).until(
#         #     EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='udbsdk_frm_normal']")))
#         frame = self.driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
#         self.driver.switch_to.frame(frame)
#         time.sleep(1)
#
#         ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
#         ele.send_keys(__username)
#
#         ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
#         ele.send_keys(__password)
#
#         time.sleep(1)
#         self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()
#
#         print("Login success")
#         time.sleep(2)
#         self.driver.switch_to.default_content()  # switch to main page
#
#     def send_msg(self, msg):
#         msg_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pub_msg_input']")))
#         # msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
#         msg_input.send_keys(msg)
#         time.sleep(3)
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'msg_send_bt'))).click()
#         # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
#         # self.driver.find_element_by_id('msg_send_bt').click()
#         time.sleep(2)
#
#     def send_advertisement(self):
#         send_frequence = self.workbook.read_cell('设置', 'A2')
#         if self.workbook.read_cell('登录', 'D%d' % self.no):
#             msg_1 = self.workbook.read_cell('登录', 'D%d' % self.no)
#             self.send_msg(msg_1)
#             time.sleep(send_frequence)
#             print('Message 1 sent!')
#             if self.workbook.read_cell('登录', 'E%d' % self.no):
#                 msg_2 = self.workbook.read_cell('登录', 'E%d' % self.no)
#                 self.send_msg(msg_2)
#                 print('Message 2 sent!')
#
#     def close_driver(self):
#         self.driver.close()
#
#     def main(self):
#         topic = self.workbook.read_cell('登录', 'C%d' % self.no)
#         total_url = self.workbook.get_max_row(topic)
#         for u in range(1, total_url):
#             url = self.workbook.read_cell(topic, 'B%d' % u)
#             print(url)
#             self.driver.get(url)
#             time.sleep(3)
#
#             if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "":
#                 print('Need to login')
#                 self.login()
#                 self.send_advertisement()
#             else:
#                 print("No need to login")
#                 self.send_advertisement()
#
#
#
# if __name__ == '__main__':
#     print( os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), "huya.xlsx"))
#     t = SEND_MSG('13250219510', '81302137hy', 2, '-hl')
#     t.main()









# 更加便利的调试，我们只需要在命令行中加入–remote-debugging-port=9222，再打开浏览器输入localhost:9222(ip为实际运行命令的ip地址)就能进入调试界面。