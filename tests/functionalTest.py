from selenium.webdriver.commmon.keys import Keys
from selenium import webdriver
import unittest
import time


class NewWorkerTest (unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_login_and_recover_password(self):

        # FooName is a worker of a company that is starting to use
        # FancyToDoApp.
        # He opens FireFox to check out the homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention the appName,
        # and the page title also mentions Login
        self.assertIn('Login', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Gestaodepraticasdiarias', header_text)
        self.assertIn('Gestaodepraticasdiarias', self.browser.title)

        # He finds himself in a LoginPage. He sees a form that asks for
        # username and password

        login_form_username = self.browser.find_element_by_class_name(
            'username')
        login_form_password = self.browser.find_element_by_class_name(
            'password')

        # He tries to enter the username and password that was given to him by
        # the Adminstrator (FooUser / CR7isGOAt)

        login_form_username.send_keys('FooUser')
        login_form_password.send_keys('Cr7isGOAT')

        # When he hits Enter, the page updates and shows an error message
        # Username or password incorrect

        login_form_password.send_keys(Keys.ENTER)
        time.sleep(1)  # waits for the page to reload

        error_message = self.browser.find_element_by_tag_name('p').text
        self.assertIn('Your username and password didn\'t match.',
                      error_message)

        # He realizes that he misspled his password and refills the forms

        login_form_username.send_keys('FooUser')
        login_form_password.send_keys('Cr7isGOAt')

        login_form_password.send_keys(Keys.ENTER)
        time.sleep(1)  # waits for the page to reload

        # After the page reloads he's taken to the homepage.
        # He notices that the page title is Home

        self.assertIn('Home', self.browser.title)

        self.fail('Finish the test!')
        # He finds is name in the NavBar, indicating that he is logged in

        # He sees the following content in the SideBar:

        # Lorem

        # Ipsum

        # Dolor

        # Amet

        # He also sees the following content in the page body:

        # Lorem

        # Ipsum

        # Dolor

        # Amet

