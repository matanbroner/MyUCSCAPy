from src.driver.selenium import generate_driver
from src.api.my_ucsc.index import MyUCSCApi

driver = generate_driver()

user = 'mbroner'
password = 'ma97ro99ra14'

course = {
    "name": "Calculus for Science, Engineering, and Mathematics",
    "course_id": "62935",
    "disc_id": None,
    "lab_id": "62937",
    "status": "Open"
}

api = MyUCSCApi(driver)
api.log_in(user, password)
api.navigate_page("Enrollment")
enrollment_module = api.module('enrollment')
enrollment_module.add_to_cart(course)
enrollment_module.enroll(course)
