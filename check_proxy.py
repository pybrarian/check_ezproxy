#!/usr/bin/env python3

import argparse
import os
import sys

import gevent.monkey
import gevent

import checks
from config import cfg
import places
from registration import places_map, checks_map

gevent.monkey.patch_all()


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
    parser.add_argument('-p', '--output_path',
                        help=('Path of location to save output with name of file. '
                              'Default is users HOME directory as check_proxy.txt.'),
                        default=os.path.join(os.path.expanduser('~'), 'check_proxy.txt'))

    return parser.parse_args()


def output(result):
    return ('Name: {name}{linebreak}'
            'Url: {url}{linebreak}'
            'Status: {status}{linebreak}'
            '---'.format(
                name=result.name,
                url=result.url,
                status=result.status,
                linebreak=os.linesep
            ))


def main(config):
    args = get_args()

    get_urls = places_map[args.urlsource]
    type_of_check = checks_map[args.type]

    print('Getting URLs from {0}.'.format(args.urlsource))
    urls = get_urls(config)

    print('Running checks on URLs.')
    threads = [gevent.spawn(type_of_check, url, config) for url in urls]
    gevent.joinall(threads)

    if args.write:
        f = open(args.output_path, 'wt')
        output_goes_to = f
    else:
        output_goes_to = sys.stdout

    print('Filtering Results.')
    for i in (thread.value for thread in threads if hasattr(thread.value, 'status')):
        print(output(i), file=output_goes_to)

    try:
        f.close()
    except NameError:
        pass


if __name__ == '__main__':
    main(cfg)
