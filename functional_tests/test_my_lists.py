from django.conf import settings
from django.contrib.auth import get_user_model

from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(
                host=self.staging_server, email=email
            )
            if type(session_key)==bytes:
                session_key=session_key.decode("utf-8")
            session_key=session_key.strip()
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = self.TEST_EMAIL
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        print('logged out')
        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
        print(f'logged in {email}')
