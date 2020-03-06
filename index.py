from src.driver.selenium import generate_driver
from src.api.my_ucsc import MyUCSCApi

driver = generate_driver()

user = 'mbroner'
password = 'ma97ro99ra14'

api = MyUCSCApi(driver)
api.log_in(user, password)