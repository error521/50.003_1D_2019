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

# run in Source\website --> python manage.py test createuser.tests.test_dashboard.AccountTestCase

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

    # def test_logout(self):
    #     # login only requires username and password
    #     existing_user = 'testuser1'
    #     existing_password = 'Password123'

    #     driver = self.driver
    #     # Open wanted link
    #     driver.get('http://127.0.0.1:8000/')
    #     # find form elements (by_name -> remember in login.html, in class tag you set name="something")
    #     username = driver.find_element_by_name('username')
    #     password = driver.find_element_by_name('password')
    #     # fill up the form
    #     username.send_keys(existing_user)
    #     time.sleep(1)
    #     password.send_keys(existing_password)
    #     time.sleep(1)
    #     #submit form
    #     login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
    #     login_button.click()
    #     time.sleep(2)

    #     logout_button = driver.find_element_by_name("logout")
    #     print(logout_button.get_attribute('href'))
    #     logout_button.click()
    #     time.sleep(1)
    #     logout_confirm = driver.find_element_by_css_selector("#logoutModal > div > div > div.modal-footer > a")
    #     logout_confirm.click()
    #     # check that it is the login page
    #     if (driver.current_url == "http://127.0.0.1:8000/"):
    #         print("successful logout")
    #         time.sleep(3)
    #         driver.quit()
    #     else:
    #         print("Did not manage to logout")
        
        


    # phase 1. Test that goes from 1. Trying to login, invalid username due to to typo, get error message, close error message, login successful, 
    # phase 2. create ticket, check if ticket has been showed in dashboard
    # phase 3. clicks on ticket and enetr forum, send 2 types of messages, one pure text and one is with file link
    # phase 4. user logs out and admin now logs in
    # pahse 5. admin clicks on that ticket and enters the chat and sends back a response
    # phase 6. user to login and quick serach ticket number
    # phase 7. user should see the new message from admin

    def test_demo_full(self):
        # setting up account details
        invalid_username = 'lauren'
        valid_username = 'twobowlsofgrace'
        valid_password = 'Password123'

        valid_adminuser = 'testadmin1'
        valid_adminpassword = "Tonight'sdinner"

        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        # phase1
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up with invalid username
        username.send_keys(invalid_username)
        time.sleep(1)
        password.send_keys(valid_password)
        time.sleep(1)
        #submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(4)

        if (driver.current_url =='http://127.0.0.1:8000/' ):
            check_errormessage = self.is_text_present("Login failure, username or password is incorrect")
            if check_errormessage == True:
                print("Phase1: 1. User has tried to login with invalid information")
                time.sleep(3)
                close_message = driver.find_element_by_class_name("close")
                close_message.click()
                time.sleep(10)
                check_errormessage_now = self.is_text_present("Login failure, username or password is incorrect")
                if (check_errormessage_now == False):
                    print("Phase1: 2. error message closed")

                    username = driver.find_element_by_name('username')
                    password = driver.find_element_by_name('password')
                    # fill up the form
                    username.send_keys(valid_username)
                    time.sleep(1)
                    password.send_keys(valid_password)
                    time.sleep(1)
                    #submit form
                    login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                    login_button.click()

                    # check the returned results
                    current_url = driver.current_url
                    if (current_url == 'http://127.0.0.1:8000/home/'):
                        print("Phase1: 3. User has logged in")
                        time.sleep(10)
                        # driver.quit()

                        # phase 2

                        # phase 3

                        # phase 4
                        logout_button = driver.find_element_by_name("logout")
                        # print(logout_button.get_attribute('href'))
                        logout_button.click()
                        time.sleep(1)
                        logout_confirm = driver.find_element_by_css_selector("#logoutModal > div > div > div.modal-footer > a")
                        print("Phase4: 1. Confirm Logout")
                        logout_confirm.click()
                        # check that it is the login page
                        if (driver.current_url == "http://127.0.0.1:8000/"):
                            print("Phase4: 2. User Successfully Logged-out")
                            time.sleep(3)

                            # Admin now logs in
                            username = driver.find_element_by_name('username')
                            password = driver.find_element_by_name('password')
                            # fill up tcurrent_window_handle
                            username.send_keys(valid_adminuser)
                            time.sleep(1)
                            password.send_keys(valid_adminpassword)
                            time.sleep(1)
                            #submit form
                            login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                            login_button.click()
                            if (driver.current_url == 'http://127.0.0.1:8000/home/'):
                                #  only Admin account has the task card
                                time.sleep(3)
                                try:
                                    view_ticket = driver.find_element_by_link_text("View Tickets")
                                    print("Phase4: 3. Admin has logged into Admin account")

                                    # phase 5
                                    # admin looks for ticket that was just created -> for simplicity sake, will look for title
                                    find_ticket = driver.find_element_by_link_text("Unable to set Jquery") # the link text should b ethe ticket na,e -> to hard code this
                                    find_ticket.click()
                                    check_right_forum = self.is_text_present("Re: Unable to set Jquery")
                                    if (check_right_forum == True):
                                        print("Phase5: 1. Admin has clicked on to the right ticket")
                                        time.sleep(2)
                                        
                                    else:
                                        print("Phase5: 1. Admin did not click on the right ticket")
                                    time.sleep(2)



                                except NoSuchElementException:
                                    print("Phase4: 3. Admin has logged into user account, hmmm something is wrong")

                        else:
                            print("Phase4: 2. User Did not Manage to logout")



                    else:
                        print("Phase1: 3. Unsuccessful Login")

                else:
                    print("Phase1: 2. issue with closing message alert")
                
            else:
                print("Phase1: 1. Wrong error/no error message")
        else:
            print("Phase: 1. Not suppose to be: " + driver.current_url)


