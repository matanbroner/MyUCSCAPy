from selenium import webdriver
import chromedriver_binary

def generate_driver(config=None):
    return webdriver.Chrome()