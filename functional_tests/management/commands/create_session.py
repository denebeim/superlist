from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from accounts.models import Token

User = get_user_model()
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    # token=Token.objects.create(email=email)
    user = User.objects.create(email=email)
    # auth.authenticate(username=token)
    # print(f'email: {user.email} auth: {user.is_authenticated}')
    # user.save()
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
