from src.driver.selenium        import generate_driver
from src.api.my_ucsc.index      import MyUCSCApi
from src.messenger.index         import Messenger

user = 'mbroner'
password = 'ma97ro99ra14'

course = {
    "name": "Mathematical Methods for Engineers I",
    "course_id": "62602",
    "disc_id": None,
    "lab_id": None,
    "status": "Open"
}

config = {
    "enrollment": {
        "quarter": "2020 Spring Quarter"
    }
}

msg = Messenger({
    "phone": "4084100240",
    "provider": "tmobile"
})
msg.login("mbroner@ucsc.edu", "ra14ro99ma97")

driver = generate_driver()

api = MyUCSCApi(driver, config)
api.log_in(user, password)
api.navigate_page("Enrollment")
enrollment_module = api.module('enrollment')
try:
    spots, course_link = enrollment_module.check_open_spots(course)
    taken, total = spots
    msg.inform_course_open(course, course_link, taken, total)
except Exception as e:
    print(e)
    pass
# enrollment_module.enroll(course)
