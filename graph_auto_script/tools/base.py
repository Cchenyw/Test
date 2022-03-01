from selenium import webdriver
from selenium.webdriver.support import expected_conditions as es
from selenium.webdriver.support.ui import WebDriverWait


def get_browser():
    browser = webdriver.Chrome()
    return browser


def get_element(browser, selector, value):
    element = WebDriverWait(driver=browser, timeout=5).until(es.presence_of_element_located((selector, value)),
                                                             message='找不到该元素')
    return element


def save_to_local(file_path, things):
    with open(file_path, 'w') as f:
        f.write(things)


def read_file(file_path):
    with open(file_path, 'r') as f:
        f.read()
