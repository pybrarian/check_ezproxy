#!/usr/bin/env python
# coding: utf-8

import requests


class KB(object):
    """
    Read and represent data from OCLC's knowledge base.

    Requires a WSKey from here:
    https://platform.worldcat.org/wskey/
    Documentation for Knowledge Base API:
    https://www.oclc.org/developer/develop/web-services/worldcat-knowledge-base-api.en.html
    Documentation for OCLC Developer Tools:
    https://www.oclc.org/developer/develop.en.html
    """
    def __init__(self, wskey):
        """Set the default parameters for KB API requests."""
        self._defaults = {'alt': 'json', 'wskey': wskey}

    @property
    def entry_search_url(self):
        return '{0}search?'.format(self.entry_base_url)

    @property
    def entry_base_url(self):
        return 'http://worldcat.org/webservices/kb/rest/entries/'

    def get_all_entries(self, collection_id, options=None):
        """
        Retrieve all entries from a given collection.
        'collection_uid' and 'itemsPerPage' are set automatically,
        adjusting through in the options dict is not advises.
        Args:
            collection_id: OCLC collection id as a string
            options: Dict of secondary options
        Returns:
            A list of dicts of the collection entries
        """
        start_index = 1
        records = []
        payload = self._get_payload(options)
        payload.update({'collection_uid': collection_id,
                        'itemsPerPage': 50})
        while True:
            payload.update({'startIndex': start_index})
            r = requests.get(self.entry_search_url, params=payload).json()
            for entry in r['entries']:
                records.append(entry)

            if len(r['entries']) < 50:
                break
            start_index += 50

        return records

    def _get_payload(self, options):
        """
        Set extra options for a request to the KB API.
        Options information can be found at:
        https://www.oclc.org/developer/develop/web-services/worldcat-knowledge-base-api.en.html
        Args:
            options: Dict of options to set. If none, return copy of the defaults.
        """
        payload = self._defaults.copy()
        try:
            payload.update(options)
        except TypeError:
            # Options is None by default
            pass
        return payload
