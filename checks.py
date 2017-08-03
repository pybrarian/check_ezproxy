from collections import namedtuple

import requests

from config import cfg
from registration import register


Checked_Url = namedtuple('Checked_Url', 'name url status')


@register('text', __name__)
def check_text(db):
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
        if cfg['ezproxy_error_text'] in database_request.text:
            db = Checked_Url(db.name, db.url, 'incorrect_config')
    except requests.exceptions.ConnectionError:
        db = Checked_Url(db.name, db.url, 'connection_error')
    except requests.exceptions.ReadTimeout:
        db = Checked_Url(db.name, db.url, 'read_timeout')
    return db

