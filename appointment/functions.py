from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse

def handle_uploaded_file(f):
    with open('mysites/static/img/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def chec_session(request):
    if 'user' in request.session:
        return True
    else:
        return redirect('/login/')

import functools


def check_admin(func):

   @functools.wraps(func)
   def wrapper(request, *args, **kwargs):
       if 'user' in request.session:
           return True
       else:
            return redirect('/login/')
       return func(request, *args, **kwargs)
   return wrapper