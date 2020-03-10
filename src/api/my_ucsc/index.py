from ...assets.urls import my_ucsc_urls
from ...assets.elements import my_ucsc_elements
from .modules.enrollment import EnrollmentModule

class MyUCSCApi:
    def __init__(self, driver, config={}):
        self.driver = driver
        self.logged_in = False
        self.config = config
        self.initialize()

    '''
    Assigns relevant modules to the main API handler
    returns: None
    '''
    def initialize(self):
        self.modules = {
            'enrollment': EnrollmentModule(self.driver, self.config["enrollment"])
        }

    '''
    Allows third party access to various attached MyUCSC modules
    @param str name: Module to access as listed in this.modules
    returns: None
    '''
    def module(self, name):
        return self.modules[name]

    '''
    Logs in to main MyUCSC page
    @param str username: A valid CruzID
    @param str password: A valid Gold Password
    returns: None
    '''
    def log_in(self, username, password):
        if(not username or not password):
            raise self._error("Invalid Login Credentials")
        
        # Complete username, password inputs
        self.driver.get(my_ucsc_urls["my_ucsc_main"])
        form = self.driver.find_element_by_class_name("login")
        user = form.find_element_by_id("username").send_keys(username)
        password = form.find_element_by_id("password").send_keys(password)
        submit = form.find_element_by_name("_eventId_proceed").click()

        # Duo (TFA) will load into the current frame window
        if(my_ucsc_urls["my_ucsc_login"] in self.driver.current_url):
            self._complete_tfa("push")

        complete_login = self.driver.find_element_by_xpath("//*[@id=\"shibSubmit\"]").click()
        self.logged_in = True

    '''
    Navigates to a page from the MyUCSC landing page
    @param str name: Page name to access
    returns: None
    '''
    def navigate_page(self, name):
        try:
            self._verify_logged_in()
            self.driver.get(my_ucsc_urls["landing_page"])
            self.driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(name)).click()
        except e:
            raise self._error("Page {} Not Found".format(name))
    

    '''
    Completes Duo TFA Authentication
    @param str method: Auth method of choice
        - "push", "phone", or "passcode"
    returns: None
    '''
    def _complete_tfa(self, method):
        tfa_frame = self.driver.find_element_by_id(my_ucsc_elements["duo_iframe"])
        self.driver.switch_to.frame(tfa_frame)
        auth_method = self.driver.find_element_by_xpath("//*[@class=\"row-label {}-label\"]".format(method))
        remember_me = self.driver.find_element_by_name(my_ucsc_elements["duo_checkbox"]) \
            .click()
        auth_method.find_element_by_class_name("positive") \
            .click()
        self.driver.switch_to.default_content()

    '''
    Helper method to prevent API calls whilst not logged in
    returns: None
    '''
    def _verify_logged_in(self):
        if(not self.logged_in):
            raise self._error("Log In Required")

    '''
    Error formatter for unqiue class errors
    returns: str formatted error
    '''       
    def _error(self, message):
        return Exception("MyUCSCApi: " + message)
        
