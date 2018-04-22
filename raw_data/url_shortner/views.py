# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
import random

from django.shortcuts import render, redirect
from django.http import Http404

from forms import URLShortnerForm
from models import UrlShortner

# Create your views here.


def id_generator(size=8, chars=string.ascii_lowercase):
    """
    Generate url shorter
    :param size:
    :param chars:
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


def check_url_exits(url):
    """
    Checks if urls exists or not
    :param url:
    :return:
    """
    try:
        short_url_object = UrlShortner.objects.get(short_url=url)
        if short_url_object:
            return None
    except UrlShortner.DoesNotExist:
        return url


def home(request):
    """
    Index page where user can generate url shorter
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = URLShortnerForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data.get("long_url", "").strip()
            short_url = form.cleaned_data.get("short_url", None)

            if short_url:

                short_url = short_url.strip()
            else:
                short_url = id_generator()

            while True:
                short_url = check_url_exits(short_url)

                if short_url:
                    break
                else:
                    short_url = id_generator()

            url_shorter_object = UrlShortner()
            url_shorter_object.long_url = long_url
            url_shorter_object.short_url = short_url
            url_shorter_object.save()
            short_url = "http://localhost:8000/%s/" % short_url
            return render(request, "success.html", locals())

    else:
        form = URLShortnerForm()
    return render(request, "index.html", locals())


def url_redirect(request, short_url):
    """
    redirecting to log url
    :param request:
    :param short_url
    :return:
    """
    if short_url:
        try:
            short_url_object = UrlShortner.objects.get(short_url=short_url)
            if short_url_object:
                return redirect(short_url_object.long_url)
        except UrlShortner.DoesNotExist:
            raise Http404


def url_not_found(request):
    """

    :param request:
    :return:
    """
    return render(request, "404.html")
