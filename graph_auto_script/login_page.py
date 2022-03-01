from tools import base
from selenium.webdriver.common.by import By


def login_page(url):
    if url == "":
        browser = base.get_browser()
        browser.get('http://user-uat.tangees.com/users/sign-in')
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


if __name__ == "__main__":
    login_page(url="")
