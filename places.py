#!/usr/bin/env python3
"""Get a list of Record tuples from different sources."""

from collections import namedtuple

import requests

from kb import KB
from registration import register

# Checks using this ask for a name and url property
Record = namedtuple('Record', 'name url')


def build_record_with_appropriate_proxy(api_record, config):
    url = api_record['url']
    if int(api_record['meta']['enable_proxy']):
        url = config['ezproxy_prefix'] + url
    return Record(api_record['name'], url)


@register('libguides', __name__)
def get_from_libguides(config):
    """
    Make a list of records scraped from university LibGuide A-Z list.

    :return: A list of Record named tuples
    """
    r = requests.get(config['libguides_api_url']).json()
    return [build_record_with_appropriate_proxy(x, config) for x in r]


@register('oclc', __name__)
def get_from_oclc(config):
    """
    Get all WSU online journals from the Knowledge base.

    Uses a connection to the Knowledge Base API as an implicit argument

    :return: A list of Record named tuples

    Nested list comprehension can be read just like nested for loop going down
    """
    kb = KB(config['kb_wskey'])

    return [Record(entry['title'], url['href'])
            for entry in kb.get_all_entries(config['kb_collections'])
            for url in entry['links']
            if 'rel' in url and url['rel'] == 'canonical']
