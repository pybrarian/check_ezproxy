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
    url = check_and_prepend_proxy(db.url)
    try:
        database_request = requests.get(url, timeout=10)
        if cfg['ezproxy_error_text'] in database_request.text:
            db = Checked_Url(db.name, db.url, 'incorrect_config')
    except requests.exceptions.ConnectionError:
        db = Checked_Url(db.name, db.url, 'connection_error')
    except requests.exceptions.ReadTimeout:
        db = Checked_Url(db.name, db.url, 'read_timeout')
    return db


def check_and_prepend_proxy(url):
    """
    See if link needs a proxy prefix and add it if so.

    Links pulled from LibGuides will smartly have the proxy, as does anything
    with the proxy prefix. For anything else, we need to add the proxy prefix
    to ensure all links are checking for proper configuration.

    :param url: String representation of a URL
    :return: A string representation of a URL with the proxy prefix
    """
    if cfg['ezproxy_prefix'] not in url:
        url = '{}{}'.format(cfg['ezproxy_prefix'], url)
    return url
