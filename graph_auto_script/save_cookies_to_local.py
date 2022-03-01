import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as es
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Edge()
# 显示等待
driver.get('http://user-dev4.tangees.com/users/sign-in')
login_button = WebDriverWait(driver, timeout=5).until(
    es.presence_of_element_located((By.TAG_NAME, 'button')))
user_inputs = driver.find_elements(By.TAG_NAME, 'input')
# username
user_inputs[0].send_keys('17520544566')
# password
user_inputs[1].send_keys('17520544566Cyw')
# login button
login_button.click()
# 获取cookies,转为json
login_cookies = driver.get_cookies()
jsonCookies = json.dumps(login_cookies)
# 保存cookies到本地
with open('./my_cookies.txt', 'w') as f:
    f.write(jsonCookies)
time.sleep(3)
driver.quit()
