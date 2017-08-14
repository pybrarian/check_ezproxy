#!/usr/bin/env python

from collections import namedtuple

import requests

from .registration import register

Checked_Url = namedtuple('Checked_Url', 'name url status')
this_module = 'checks'


@register('text', this_module)
def check_text(db, config):
    """
    Send a get request, see if EZProxy error message returned.

    Web address sends a 200 code even if proxy misconfigured, so must check
    text. If the url is from LibGuides or it already has the proxy prefix,
    just take the url, else prepend the Proxy.

    :param db: A named tuple or class representing information about a
        database, must have a name and a url property
    :return: The passed in parameter
    """
    try:
        database_request = requests.get(db.url, timeout=10)
        if config['ezproxy_error_text'] in database_request.text:
            db = Checked_Url(db.name, db.url, 'Incorrect Proxy Configuration')
    except requests.exceptions.ConnectionError:
        db = Checked_Url(db.name, db.url, 'Connection Error')
    except requests.exceptions.ReadTimeout:
        db = Checked_Url(db.name, db.url, 'Read Timeout')
    return db


@register('links', this_module)
def check_link(db, config):
    try:
        database_request = requests.head(db.url, timeout=10)
        if database_request.status_code == 404:
            db = Checked_Url(db.name, db.url, 'Invalid URL')
    except requests.exceptions.ConnectionError:
        db = Checked_Url(db.name, db.url, 'Connection Error')
    except requests.exceptions.ReadTimeout:
        db = Checked_Url(db.name, db.url, 'Read Timeout')
    return db
