from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()
WILLING_TEST_SUBJECT = 'edith@example.com'


class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            'no_such_token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = WILLING_TEST_SUBJECT
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = WILLING_TEST_SUBJECT
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    def test_gets_user_by_email(self):
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email=WILLING_TEST_SUBJECT)
        found_user = PasswordlessAuthenticationBackend().get_user(WILLING_TEST_SUBJECT)
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(WILLING_TEST_SUBJECT)
        )
