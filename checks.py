import os

import requests

from config import cfg
from registration import register


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
    print('Checking {0}'.format(db.name.encode('ascii', 'replace')))
    url = check_and_prepend_proxy(db.url)
    try:
        database_request = requests.get(url, timeout=10)
        if cfg['ezproxy_error_text'] in database_request.text:
            MISCONFIGURED_DATABASES.append(db)
    except requests.exceptions.ConnectionError:
        MISCONFIGURED_DATABASES.append(db)
    except requests.exceptions.ReadTimeout:
        MISCONFIGURED_DATABASES.append(db)
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
