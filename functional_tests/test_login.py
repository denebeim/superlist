import os
import poplib
import time

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
        if self.staging_server:
            test_email = os.getenv('TEST_EMAIL')
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(test_email)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # a message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                'Check your email',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        )

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in mail body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        time.sleep(1)  # wait for some race condition
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        # inbox.set_debuglevel(2)
        try:
            inbox.user(test_email)
            p = os.getenv('TEST_EMAIL_SECRET')
            inbox.pass_(p)
            while time.time() - start < 60:
                # get 10 latest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
                inbox.quit()
