from django.test import LiveServerTestCase 
from django.contrib.sessions.models import Session 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import * 
import time 
import re 
 
 
# run in Source\website --> python manage.py test createuser.tests.test_register.AccountTestCase 
 
class AccountTestCase(LiveServerTestCase): 
    # To initialise the driver 
    def setUp(self): 
        self.driver = webdriver.Firefox() 
        super(AccountTestCase, self).setUp() 
         
    # Terminate the session 
    def tearDown(self): 
        self.driver.quit() 
        super(AccountTestCase, self).tearDown() 
 
    # to check is  text is present 
    def is_text_present(self, text): 
        return str(text) in self.driver.page_source 
 
    def test_login_register_login(self): 
        create_user = 'testuser14' 
        create_phoneNumber = '12345678' 
        create_email = 'testuser14@mail.com' 
        create_password = 'Password123' 
 
        driver = self.driver 
        # Open wanted link 
        driver.get('http://127.0.0.1:8000/') 
 
        # get and click on register link 
        view_ticket = driver.find_element_by_link_text("Don't have account? Register Here!") 
        view_ticket.click() 
        time.sleep(2) 
        print(driver.current_url) 
 
        #find the form element 
        username = driver.find_element_by_name('username') 
        phoneNumber = driver.find_element_by_name('phoneNumber') 
        email = driver.find_element_by_name('email') 
        password = driver.find_element_by_name('password') 
        notify_email = driver.find_element_by_name('notify_email') 
        notify_sms = driver.find_element_by_name('notify_sms') 
 
        #  fill up fomr 
        username.send_keys(create_user) 
        time.sleep(2) 
        phoneNumber.send_keys(create_phoneNumber) 
        time.sleep(2) 
        email.send_keys(create_email) 
        time.sleep(2) 
        password.send_keys(create_password) 
        time.sleep(2) 
        notify_email.click() 
        notify_sms.click() 
        time.sleep(3) 
 
        #submit form 
        register_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div[2]/div/button") 
        register_button.click() 
        if (driver.current_url == "http://127.0.0.1:8000/createuser/"): 
            print("1. registration unsuccessful") 
            driver.quit() 
        if (driver.current_url == "http://127.0.0.1:8000/"): 
            print("1. successful registration") 
            time.sleep(2) 
 
            # start loging in  
            username = driver.find_element_by_name('username') 
            password = driver.find_element_by_name('password') 
            # fill up the form 
            username.send_keys(create_user) 
            time.sleep(1) 
            password.send_keys(create_password) 
            time.sleep(1) 
            #submit login form 
            login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button") 
            login_button.click() 
 
            current_url = driver.current_url 
            if (current_url == 'http://127.0.0.1:8000/home/'): 
                print("2. User has logged in") 
                time.sleep(10) 
                driver.quit() 
 
            else: 
                print("2. Unsuccessful Login") 
 
    def test_find_all_links(self): 
        driver = self.driver 
         
        # Open wanted link 
        driver.get('http://127.0.0.1:8000/createuser/') 
        # get all links 
        for a in driver.find_elements_by_xpath('.//a'): 
            print("link text: " +  a.text) 
            fr = a.get_attribute('href') 
            print("Navigating to: " + fr) 
            if (fr == "http://127.0.0.1:8000/"): 
                print("linked to the right page") 
            else: 
                print("error") 
 
    def test_submit_empty_form_with_message(self): 
        driver = self.driver 
         
        # Open wanted link 
        driver.get('http://127.0.0.1:8000/createuser/') 
        # click register button 
        register_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div[2]/div/button") 
        register_button.click() 
        time.sleep(4) 
        if (driver.current_url =='http://127.0.0.1:8000/createuser/' ): 
            check_errormessage = self.is_text_present("Please fill in all input fields") 
            if check_errormessage == True: 
                print("User has tried to submit an empty form") 
                time.sleep(3) 
            else: 
                print("Wrong error/no error message") 
        else: 
            print("Not suppose to be: " + driver.current_url) 
 
 
 
 
         
 
 
