#!/usr/bin/env python3

import argparse
import json
import os
import pickle
import sys

import gevent.monkey
import gevent

import checks
import places
from registration import places_map, checks_map

try:
    from config import cfg
except ImportError:
    pass

gevent.monkey.patch_all()


class ConfigError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return ('There is an error in your configuration.'
                if self.message is None else self.message)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--urlsource',
                        help='Where to get database URLs.',
                        default='libguides',
                        choices=places_map.keys())
    parser.add_argument('-k', '--kbart',
                        help='Path to a KBART file to check.')
    parser.add_argument('-t', '--type',
                        help='Type of check to run.',
                        default='text',
                        choices=checks_map.keys())
    parser.add_argument('-w', '--write',
                        help='Write to file.',
                        action='store_true')
    parser.add_argument('-f', '--output_file',
                        help=('Path of location to save output with name of file. '
                              'Default is users HOME directory as check_proxy.txt.'),
                        default=os.path.join(os.path.expanduser('~'), 'check_proxy.txt'))
    parser.add_argument('-p', '--proxy',
                        help='Force the presence or absence of a proxy prefix. '
                             'Without the tool will try to determine which urls to proxy.',
                        choices=('force', 'no_proxy'))
    parser.add_argument('-c', '--config-file',
                        help='Full path to a JSON file containing necessary config.')
    parser.add_argument('-s', '--save-config',
                        help='For use with -c option. Saves the configuration '
                             'file passed in so you don\'t have to keep passing it.',
                        action='store_true')
    parser.add_argument('--flush-config',
                        help='Flush out any saved config. Will only get rid of '
                             'configs imported from JSON, you have to edit '
                             'Python-based config directly. Can be used in same '
                             'command with a new config.',
                        action='store_true')
    return parser


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


def pickle_config(config, pickle_path):
    with open(pickle_path, 'wb') as w:
        pickle.dump(config, w)


def unpickle_config(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get_json_config(args, pickle_path):
    try:
        path_to_file = os.path.abspath(os.path.expanduser(args.config_file))
        with open(path_to_file, 'r') as f:
            config = json.load(f)
            if args.save_config:
                pickle_config(config, pickle_path)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(
            'Your config file was not found. Check your path or rename '
            'config-template.py to config.py and change defaults.')


def get_config(args):
    pickle_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.pickle')

    if args.flush_config and os.path.exists(pickle_file):
        os.remove(pickle_file)
    if os.path.exists(pickle_file):
        if args.config_file:
            raise ConfigError('You have a saved config. Use --flush-config with '
                              '--config [file] and optionally -s if you want to '
                              'load a new configuration file.')
        config = unpickle_config(pickle_file)
    elif args.config_file:
        config = get_json_config(args, pickle_file)
    else:
        try:
            config = cfg
        except NameError:
            raise ConfigError('Can not find a usable configuration. Please '
                              'check your configs or consult the documentation')
    return config


def main(config, args, output=output):
    get_urls = places_map[args.urlsource]
    type_of_check = checks_map[args.type]

    if args.write:
        f = open(args.output_file, 'wt')
        output_goes_to = f
    else:
        output_goes_to = sys.stdout

    print('Getting URLs from {0}.'.format(args.urlsource))
    urls = get_urls(config, args.proxy, args.kbart)

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


if __name__ == '__main__':
    args = get_args().parse_args()
    cfg = get_config(args)
    main(cfg, args, output)
