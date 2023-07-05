import sys
from pprint import pprint

from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect

from accounts.models import User
from lists.forms import ItemForm, ExistingListItemForm
from lists.models import List


# Create your views here.
def home_page(request):
    if settings.SESSION_COOKIE_NAME in request.COOKIES.keys():
        session=SessionStore()
        email=session.get(request.COOKIES[settings.SESSION_COOKIE_NAME])
        user=User.objects.get(email=email)
        user.is_authenticated = True
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
