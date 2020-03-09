from ....assets.urls import my_ucsc_urls

class ApiModule:
    def __init__(self, driver, page):
        self.driver = driver
        self.page = page

    def change_tab(self, name):
        try:
            self.driver.switch_to.default_content()
            self.driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(name)).click()
        except:
            raise Exception("ApiModule: Tab {} Not Found".format(name))

    def _verify_page(self):
        return self.page in self.driver.current_url 