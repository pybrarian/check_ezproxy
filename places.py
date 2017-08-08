#!/usr/bin/env python3
"""Get a list of Record tuples from different sources."""

from collections import namedtuple
import os

import pykbart
import requests

from kb import KB
from registration import register

# Checks using this ask for a name and url property
Record = namedtuple('Record', 'name url')


def libguides_record_with_appropriate_proxy(api_record, config, proxy=None):
    url = api_record['url']
    if proxy == 'no_proxy':
        pass
    elif proxy == 'force' or int(api_record['meta']['enable_proxy']):
        url = config['ezproxy_prefix'] + url
    return Record(api_record['name'], url)


@register('libguides', __name__)
def get_from_libguides(config, proxy=None):
    """
    Make a list of records from university LibGuide A-Z list.

    :return: A list of Record named tuples
    """
    r = requests.get(config['libguides_api_url']).json()
    return [libguides_record_with_appropriate_proxy(x, config, proxy) for x in r]


def oclc_record_with_appropriate_proxy(api_entry, config, proxy=None):
    for url in api_entry['links']:
        if 'rel' in url and url['rel'] == 'canonical':
            return Record(api_entry['title'],
                          url['href'] if proxy == 'no_proxy' else config['ezproxy_prefix'] + url['href'])


@register('oclc', __name__)
def get_from_oclc(config, proxy=None):
    """
    Get all online journals from the Knowledge base.

    Uses a connection to the Knowledge Base API as an implicit argument

    :return: A list of Record named tuples
    """
    kb = KB(config['kb_wskey'])
    return [oclc_record_with_appropriate_proxy(entry, config, proxy)
            for collection in config['kb_collections']
            for entry in kb.get_all_entries(collection)]


def kbart_with_appropriate_proxy(record, config, proxy):
    return Record(record.title, record.url if proxy == 'no_proxy' else config['ezproxy_prefix'] + record.url)


@register('kbart', __name__)
def get_from_kbart(config, proxy=None, file_path=None):
    path_to_file = os.path.abspath(os.path.expanduser(file_path))
    with pykbart.KbartReader(path_to_file) as reader:
        return [kbart_with_appropriate_proxy(record, config, proxy)
                for record in reader]
