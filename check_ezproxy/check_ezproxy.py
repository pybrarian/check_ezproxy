#!/usr/bin/env python

import os
import sys

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from .args import get_args
from .get_config import get_config
from .registration import places_map, checks_map
import check_ezproxy.places
import check_ezproxy.checks


__version__ = '0.2.1'


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


def run(config, args, output=output):
    # if args.kbart and not args.:
    #     args.urlsource = 'kbart'
    get_urls = places_map[args.urlsource]
    type_of_check = checks_map[args.type]

    if args.write:
        f = open(args.output_file, 'wt')
        output_goes_to = f
    else:
        output_goes_to = sys.stdout

    print('Getting URLs from {0}.'.format(args.urlsource))
    urls = get_urls(config, args.proxy, file_path=args.kbart)

    print('Running checks on URLs.')
    threads = [gevent.spawn(type_of_check, url, config) for url in urls]
    gevent.joinall(threads)

    print('Filtering Results.')
    for error_result in (thread.value for thread in threads if hasattr(thread.value, 'status')):
        print(output(error_result), file=output_goes_to)

    try:
        f.close()
    except NameError:
        pass


def main():
    args = get_args().parse_args()
    cfg = get_config(args)
    run(cfg, args, output)
