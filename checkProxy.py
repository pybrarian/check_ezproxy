#!/usr/bin/env python

import argparse
from concurrent import futures
import os
from pprint import pprint

import checks
from constants import MAX_WORKERS, MISCONFIGURED_DATABASES, HOME
import places
from registration import places_map, checks_map


def concurrent_check(db_list, action_to_take):
    """
    Check databases in db_list for proxy configuration.

    :param db_list: list of db objects with a name and url property
    :param action_to_take: function reference to process the database checks
    :return: length of the list of databases we just successfully went through
    """
    workers = min(MAX_WORKERS, len(db_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(action_to_take, db_list)
    return len(list(res))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--urlsource',
                        help='Where to get database URLs.',
                        default='libguides',
                        choices=places_map.keys())
    parser.add_argument('-t', '--type',
                        help='Type of check to run.',
                        default='text',
                        choices=checks_map.keys())
    parser.add_argument('-w', '--write',
                        help='Write to file.',
                        action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()

    if args.write and args.type == 'screenshot':
        raise TypeError('Cannot combine screenshot and write operations.')

    # Get the references to the specified functions.
    get_urls = places_map[args.urlsource]
    type_of_check = checks_map[args.type]

    urls = get_urls()
    concurrent_check(urls, type_of_check)

    if MISCONFIGURED_DATABASES and not args.write:
        print('The following databases are not or are wrongly configured:\n')
        pprint(MISCONFIGURED_DATABASES)

    if args.write:
        filename = os.path.join(HOME, 'misconfigured_databases.txt')
        with open(filename, mode='wt', encoding='utf-8') as w:
            for db in MISCONFIGURED_DATABASES:
                w.write('Name: {0}, Url: {1}\n'.format(db.name, db.url))

    print('All done.')
