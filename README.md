## MyUCSC APy

![logo photo](src/assets/images/logo.jpg)

A robust API for interaction with the MyUCSC enrollment system. 
Very much still a work in progress.

**Stability:** Not stable (03/10/2020)

**I am not responsible for any issues with registration or repercussions involved with using this service. Use at your own discretion.**

**Features**

 - **Auto Enroll:** Enables users to set up an "auto-enroller" which crawls the class class search with a given course set and informs the user through a text message. 

**To Do**

 - [ ] GUI for interaction
 - [ ] Clean up API interaction and set up
 - [ ] Timer setup for auto-enroller

**Example Usage**
This will be drastically reworked as development continues.
```python
from src.driver.selenium 	import generate_driver
from src.api.my_ucsc.index 	import MyUCSCApi
from src.messenger.index 	import Messenger

user =  'cruz-id'
password =  'gold-password'

course = {
"name": "Mathematical Methods for Engineers I",
"course_id": "62602",
"disc_id": "62607",
"lab_id": "62610",
"status": "Open"
}

config = {
	"enrollment": {
		"quarter": "2020 Spring Quarter"
	}
}

msg =  Messenger({
	"phone": "4084100240",
	"provider": "tmobile"
})

msg.login("cruz-id@ucsc.edu", "blue-password")
driver =  generate_driver()

api =  MyUCSCApi(driver, config)
api.log_in(user, password)
api.navigate_page("Enrollment")
enrollment_module = api.module('enrollment')

try:
	spots, course_link = enrollment_module.check_open_spots(course)
	taken, total = spots
	msg.inform_course_open(course, course_link, taken, total)
except  Exception  as e:
	print(e)
```
