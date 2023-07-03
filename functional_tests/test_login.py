from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest, wait

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awsome superlists site and notices a 'Log in' section in
        # the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(self.WILLING_TEST_SUBJECT)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # a message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                'Check your email',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        )

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(self.WILLING_TEST_SUBJECT, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in mail body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=self.WILLING_TEST_SUBJECT)

        # Now she logs out
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=self.WILLING_TEST_SUBJECT)
