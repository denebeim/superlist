from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse

from accounts.models import Token


# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    print(f'email: {email}')
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    print(url)
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
        fail_silently=False,
    )
    print('Mail Sent')
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    uid = request.GET.get('token')
    user = auth.authenticate(username=uid)
    if user:
        auth.login(request, user)
    return redirect('/')
