import time

from tools import base
from selenium.webdriver.common.by import By

browser = base.get_browser()
browser.get('http://user-dev4.tangees.com/users/sign-in')

# login_page
# username
username = base.get_element(browser, By.XPATH,
                            '//*[@id="user-login-wrapper"]/div/div/div/section[2]/form/div[1]/div/div/span/span/span/span[2]/input')
username.send_keys('17520544566')
# password
password = base.get_element(browser, By.XPATH,
                            '//*[@id="user-login-wrapper"]/div/div/div/section[2]/form/div[2]/div/div/span/span/input')
password.send_keys('17520544566Cyw')
# login_button
login_button = base.get_element(browser, By.TAG_NAME, 'button')
login_button.click()

# personal_center_page
# smart_voice_button
smart_voice_button = base.get_element(browser, By.XPATH,
                                      '//*[@id="app-content"]/div[1]/div[2]/div/div[1]/div[2]/div[2]/a[3]')
smart_voice_button.click()

# smart_voice_page
# my_graph_button
my_graph_button = base.get_element(browser, By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[1]/div/div/ul/li[4]/a')
my_graph_button.click()

# my_graph_page
# create_new_graph_button
create_new_graph_button = base.get_element(browser, By.XPATH, '//*[@id="app-content"]/div/div/div[1]/div/button')
create_new_graph_button.click()

# 选择弹窗元素
tc = base.get_element(browser, By.CLASS_NAME, 'ant-modal-content')
# 话术名称
base.get_element(tc, By.CLASS_NAME, 'ant-input').send_keys('话术{}')
# 话术模板 --默认意向邀约模板
base.get_element(browser, By.XPATH,
                 '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/div/span/div/label[1]/span[1]/input').click()
# 播音方式
base.get_element(browser, By.XPATH,
                 '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/form/div[3]/div[2]/div/span/div/label/span[1]/input').click()
# 下一步
base.get_element(browser, By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

# wait and exit
time.sleep(3)
browser.quit()
