from ..assets.urls import my_ucsc_login

class MyUCSCApi:
    def __init__(self, driver):
        self.driver = driver
        self.logged_in = False

    def log_in(self, username, password):
        if(not username or not password):
            raise self._error("Invalid Login Credentials")
        
        # Complete username, password inputs
        self.driver.get(my_ucsc_login)
        form = self.driver.find_element_by_class('login')
        user = form.find_element_by_id('username').send_keys(username)
        password = form.find_element_by_id('password').send_keys(password)
        submit = form.find_element_by_name('_eventId_proceed').click()

        # Duo (TFA) will load into the current frame window
        if(self.driver.current_url() == my_ucsc_login):
            self._complete_tfa()
    
    def _complete_tfa():
        

    def _verify_logged_in(self):
        if(not self.logged_in):
            raise self._error("Log In Required")

    def _error(self, message):
        return "MyUCSCApi: " + message
