from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException
import time
from ticket_creation.models import All_Tickets, Ticket, Ticket_Details


class CreateTicketByUser(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(CreateTicketByUser, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(CreateTicketByUser, self).tearDown()

    def test_CreateTicketByUser(self):
        user_username= 'Tired'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(2)
        print("User has logged in")

        # User has logged in
        # User clicks Create Ticket link to create ticket
        link_create_ticket = driver.find_element_by_link_text('Create Ticket')
        link_create_ticket.click()
        time.sleep(2)

        ticket_title = 'Help'
        ticket_description = 'Send Help'
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        ticket_title_field = driver.find_element_by_name("title")
        ticket_title_field.send_keys(ticket_title)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ticket_description_field = driver.find_element_by_id('description')
        # wait = WebDriverWait(driver,10)
        # wait.until(EC.visibility_of(ticket_description_field))
        # wait.until(EC.element_to_be_clickable(ticket_description_field))

        ticket_description_field.send_keys(ticket_description)
        time.sleep(1)



        # wait = WebDriverWait(driver, 20)
        # wait.until(EC.visibility_of_element_located((By.NAME, "description")))
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        # ticket_description_field.click()
        #ticket_description_field.send_keys(ticket_description)
        #time.sleep(1)
        ticket_create_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div/div/div/button")
        ticket_create_button.click()
        expectedMessage = 'x\nTicket creation success'
        message = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div")
        msg_text = message.text
        self.assertTrue(message)
        self.assertEqual(msg_text, expectedMessage)
        driver.quit()


class ViewTicketByAdmin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(ViewTicketByAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ViewTicketByAdmin, self).tearDown()

    def test_ViewTicketByAdmin(self):
        user_username = 'joe'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(2)
        print("Admin has logged in")

        # Admin has logged in
        # Admin clicks View all tickets
        time.sleep(1)
        # link_view_ticket = driver.find_element_by_link_text("View Tickets")
        # link_view_ticket.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ticket_link = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div/table/tbody/tr[1]/td[3]/a")
        previousRead = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div/table/tbody/tr[1]/td[4]").text
        id = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div/table/tbody/tr[1]/td[1]").text
        time.sleep(1)
        ticket_link.click()
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/home/")
        time.sleep(3)
        newRead = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[3]/div/table/tbody/tr[{}]/td[4]".format(id)).text
        self.assertNotEqual(previousRead,newRead)

        driver.quit()


class ResolveTicketByAdmin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(ResolveTicketByAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ResolveTicketByAdmin, self).tearDown()

    def test_ResolveTicketByAdmin(self):
        user_username = 'joe'
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
        print("Admin has logged in")

        # Admin has logged in
        # Admin clicks View all tickets link to create ticket
        link_create_ticket = driver.find_element_by_link_text('View all tickets')
        time.sleep(1)
        link_create_ticket.click()
        time.sleep(1)
        link_view_ticket = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[3]/a")
        previousResolve = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[5]").text
        id = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[1]").text
        time.sleep(1)
        link_view_ticket.click()
        time.sleep(1)
        resolve_button = driver.find_element_by_xpath("/html/body/div[1]/a")
        resolve_button.click()
        time.sleep(1)
        alert_obj = driver.switch_to.alert
        msg = alert_obj.text
        print("Alert shows following message: " + msg)
        alert_obj.accept()
        time.sleep(1)
        # driver.get("http://127.0.0.1:8000/ticket_creation/display/")
        # time.sleep(3)
        newResolve = driver.find_element_by_xpath("/html/body/table/tbody/tr[{}]/td[5]".format(id)).text
        self.assertNotEqual(previousResolve, newResolve)

        driver.quit()


class CancelResolveTicketByAdmin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(CancelResolveTicketByAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(CancelResolveTicketByAdmin, self).tearDown()

    def test_ResolveTicketByAdmin(self):
        user_username = 'joe'
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
        print("Admin has logged in")

        # Admin has logged in
        # Admin clicks View all tickets link to create ticket
        link_create_ticket = driver.find_element_by_link_text('View all tickets')
        time.sleep(1)
        link_create_ticket.click()
        time.sleep(1)
        link_view_ticket = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[3]/a")
        previousResolve = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[5]").text
        id = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[1]").text
        time.sleep(1)
        link_view_ticket.click()
        time.sleep(1)
        resolve_button = driver.find_element_by_xpath("/html/body/div[1]/a")
        resolve_button.click()
        time.sleep(1)
        alert_obj = driver.switch_to.alert
        msg = alert_obj.text
        print("Alert shows following message: " + msg)
        alert_obj.dismiss()
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/ticket_creation/display/")
        # time.sleep(3)
        newResolve = driver.find_element_by_xpath("/html/body/table/tbody/tr[{}]/td[5]".format(id)).text
        self.assertEqual(previousResolve, newResolve)

        driver.quit()

