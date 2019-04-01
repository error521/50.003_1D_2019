from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()


    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def is_text_present(self, text):
        return str(text) in self.selenium.page_source

    def test_register(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/createuser/')
        #find the form element
        username = selenium.find_element_by_name('username')
        phoneNumber = selenium.find_element_by_name('phoneNumber')
        email = selenium.find_element_by_name('email')
        password = selenium.find_element_by_name('password')



        #Fill the form with data
        username.send_keys('JohnSmith')
        phoneNumber.send_keys('12345678')
        email.send_keys('johnsmith@mail.com')
        password.send_keys('password1234')


        #submitting the form
        submit_button = selenium.find_elements_by_xpath("/html/body/div/div/div/article/form/div[5]/button")[0]
        submit_button.click()

        #check the returned result
        #assert 'Check your email' in selenium.page_source
        self.is_text_present("Please sign in")