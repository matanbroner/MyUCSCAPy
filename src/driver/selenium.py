from selenium import webdriver
import chromedriver_binary

def generate_driver(config=None):
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    return driver