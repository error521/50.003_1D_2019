from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException
import time
from ticket_creation.models import All_Tickets, Ticket, Ticket_Details


class EditProfileByUser(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(EditProfileByUser, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(EditProfileByUser, self).tearDown()

    def test_EditProfileByUser(self):
        user_username = 'Tired'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/button")
        login_button.click()
        time.sleep(2)
        print("User has logged in")
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/Profile/")
        time.sleep(2)
        phoneNumber_field = driver.find_element_by_name("phoneNumber")
        time.sleep(1)
        phoneNumber_field.send_keys('98765432')
        time.sleep(1)
        submit_new_button = driver.find_element_by_css_selector(".btn")
        submit_new_button.click()
        time.sleep(1)
        driver.quit()