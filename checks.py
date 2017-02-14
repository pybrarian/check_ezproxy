import os

import requests
from selenium import webdriver

from constants import (MISCONFIGURED_DATABASES, HOME, EZPROXY,
                       ERROR_TEXT, SCREENSHOT_LOCATION)
from registration import register


@register('screenshot', __name__)
def take_screenshot(db):
    """
    Download a screenshot of the provided page to a 'screenshots' dir.

    Directory is hardcoded to download the images as a png into a
    'screenshots' directory in the user's home.

    :param db: A named tuple or class representing information about a
        database, must have a name and a url property
    :return: The passed in parameter
    """
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    driver.set_window_size(1080, 800)

    url = check_and_prepend_proxy(db.url)
    print('Checking {0}'.format(db.name.encode('ascii', 'replace')))
    driver.get(url)

    save_screenshots_here = os.path.join(HOME,
                                         SCREENSHOT_LOCATION,
                                         '{0}.png'.format(db.name))
    driver.save_screenshot(save_screenshots_here)
    driver.quit()
    return db


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
        if ERROR_TEXT in database_request.text:
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
    if EZPROXY not in url:
        url = '{}{}'.format(EZPROXY, url)
    return url
