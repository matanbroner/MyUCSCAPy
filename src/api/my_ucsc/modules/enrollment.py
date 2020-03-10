from ....assets.urls import my_ucsc_urls
from ....assets.elements import my_ucsc_elements
from ....assets.utils import match_table_row_cell_value, table_cells, extract_numbers
from ....assets.constants import OPEN_CLASSES, ALL_CLASSES, STATUS_OPEN_IMAGE
from .index import ApiModule

from selenium.webdriver.common.keys import Keys


class EnrollmentModule(ApiModule):
    def __init__(self, driver, config):
        super().__init__(driver, my_ucsc_urls["enrollment_page"])
        self.config = config
    
    '''
    Searches for courses by name and returns an array of courses
    @param dict course
    returns: WebDriverElement course block
    ''' 
    def search_courses(self, course):
        if course["status"] not in [OPEN_CLASSES, ALL_CLASSES]:
            raise self._error("Status Passed Not Valid")

        super().change_tab("Class Search")
        self._shift_to_content_iframe()
        self.driver.find_element_by_id("reg_status") \
            .find_element_by_xpath("//*[contains(text(), '{} Classes')]".format(course["status"])) \
                .click()

        self.driver.find_element_by_id("title").send_keys(course["name"], Keys.ENTER)
        try:
            courses = self.driver.find_elements_by_class_name("panel-default")
            return courses
        except e:
            return []

    '''
    Searches for a course by its ID and returns a matching item if found
    @param dict course
    returns: WebDriverElement course block
    '''  
    def search_course_by_id(self, course):
        courses = self.search_courses(course)
        for course_block in courses:
            course_id_link = "class_id_{}".format(course["course_id"])
            try:
                course_block.find_element_by_id(course_id_link)
                return course_block
            except:
                pass
        return None

    '''
    Checks the number of open spots in a course
    @param dict course
    returns: tuple (int enrolled, int total)
    '''  
    def check_open_spots(self, course):
        course_block = self.search_course_by_id(course)
        if not course_block:
            raise self._error("Course '{} - {}' Not Found".format(course["name"], course["course_id"]))
        enrollment_text = course_block.find_element_by_xpath(my_ucsc_elements["open_spots_text"]).text
        course_link = course_block.find_element_by_id("class_id_{}".format(course["course_id"])) \
            .get_attribute("href")
        return tuple(extract_numbers(enrollment_text)), course_link
        
    '''
    Adds a course to the student's shopping cart if course is found
    @param dict course
    returns: None
    '''  
    def add_to_cart(self, course):
        course_block = self.search_course_by_id(course)
        if not course_block:
            raise self._error("Course '{} - {}' Not Found".format(course["name"], course["course_id"]))
        course_block.find_element_by_name("cart[]") \
            .find_element_by_css_selector("a") \
                .click()
        if not self._text_is_present("This class is already in your Shopping Cart"):
            verify_open = lambda self, cells: self._section_is_open(cells)
            self._select_enrollment_row(my_ucsc_elements["discussion_sections_table"], course["disc_id"], [verify_open])
            self._select_enrollment_row(my_ucsc_elements["lab_sections_table"], course["lab_id"], [verify_open])
            submit_sections = self.driver.find_element_by_name(my_ucsc_elements["submit_sections_button"]) \
                .click()
            auto_waitlist = self.driver.find_element_by_name(my_ucsc_elements["auto_waitlist_checkbox"]) \
                .click()
            finalize_add_to_cart = self.driver.find_element_by_name(my_ucsc_elements["finalize_add_to_cart_button"]) \
                .click()
        else:
            raise self._error("Course {} - {} Already Added To Shopping Cart".format(course["name"], course["course_id"]))
    
    '''
    Enrolls in a course if course is found in the student's shopping cart
    @param dict course
    returns: None
    '''  
    def enroll(self, course): 
        super().change_tab("Enrollment Shopping Cart")
        self._shift_to_content_iframe()
        self._select_term()
        find_checkbox = lambda cell: cell.find_element_by_class_name("PSCHECKBOX")
        paren_id = "({})".format(course["course_id"])
        self._select_enrollment_row(my_ucsc_elements["shopping_cart_table"], paren_id, [], find_checkbox, "td/div/span/a", '.')
        enroll_next = self.driver.find_element_by_name(my_ucsc_elements["enroll_table_button"]) \
            .click()
        if self._text_is_present("You do not have a valid enrollment appointment at this time."):
            raise self._error("Unable To Enroll Due To Invalid Appointment Time")
        finalize_enroll = self.driver.find_element_by_xpath(my_ucsc_elements["finalize_enroll_button"]) \
            .click()
        self._verify_enrollment_status(course)

    '''
    Selects a table row by providing a valid table's <tbody> xpath and an ID, should be run through add_to_cart() or enroll()
    Allows use of an array of validator funtions, which must have self and cells passed to them.
    Allows input selecyed to be custom, by default find an <input> in the first cell in the row
    Expects table value to validate to be in index 1 of cells
    @param str table_path
    @param str select_id
    @param [f()] validators
    returns: None
    ''' 
    def _select_enrollment_row(self, table_path, select_id, validators=[], input_selected=None, cell_value_path=None, contains_elem=None):
        if not select_id:
            return
        table = self.driver.find_element_by_xpath(table_path)
        row, cells = match_table_row_cell_value(table, 1, select_id, cell_value_path, contains_elem)
        if not row:
            raise self._error("ID {} Not Found".format(select_id))
        for validator in validators:
            if not validator(self, cells):
                raise self._error("ID {} Does Not Pass Validation".format(select_id))
        if not input_selected:
            select = cells[0].find_element_by_css_selector("input") \
                .click()
        else:
            input_selected(cells[0]) \
                .click()
    
    def _verify_enrollment_status(self, course):
        table = self.driver.find_element_by_xpath(my_ucsc_elements["enroll_status_table"])
        cells_rows = table_cells(table)
        for cells_row in cells_rows:
            cells = cells_row[1]
            status_image_src = cells[2].find_element_by_css_selector("img") \
                .get_attribute("src")
            if my_ucsc_elements["enroll_status_error_src"] in status_image_src:
                error_message = cells[1].find_element_by_css_selector("div").text
                raise self._error("Registration Failed - \"{}\"".format(error_message))

    '''
    Verifies that a given section has available spot through checking the image src of the status column, should be run through _select_section()
    @param [WebDriverElement] section_cells
    returns: bool 
    ''' 
    def _section_is_open(self, section_cells):
        image_status_src = section_cells[6].find_element_by_css_selector("img") \
            .get_attribute("src")
        return STATUS_OPEN_IMAGE in image_status_src

    '''
    Selects the registration term as passed by the config in the contructor
    returns: None
    '''
    def _select_term(self):
        if self._text_is_present("Select Term"):
            self._select_enrollment_row(my_ucsc_elements["select_term_table"], self.config["quarter"])
            self.driver.find_element_by_xpath(my_ucsc_elements["select_term_button"]) \
                .click()
    '''
    Checks if an error message is present on the screen
    @param str message
    returns: bool
    '''
    def _text_is_present(self, message):
        try:
            self.driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(message))
            return True
        except:
            return False

    '''
    Shifts to the main content iFrame located in the enrollment section
    returns: None
    '''
    def _shift_to_content_iframe(self):
        frame = self.driver.find_element_by_class_name(my_ucsc_elements["enrollment_iframe"])
        self.driver.switch_to.frame(frame)

    '''
    Error formatter for unqiue class errors
    returns: str formatted error
    '''       
    def _error(self, message):
        return Exception("EnrollmentModule: " + message)

    

    