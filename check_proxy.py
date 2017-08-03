#!/usr/bin/env python

import argparse
import os
from pprint import pprint

import checks
from config import cfg
import places
from registration import places_map, checks_map


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

    print('All done.')
