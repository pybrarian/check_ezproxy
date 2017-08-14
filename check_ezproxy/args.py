import argparse
import os

from .registration import checks_map, places_map


def get_args():
    places_to_check = places_map.keys()
    checks_to_do = checks_map.keys()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--urlsource',
                        help='where to get database URLs. Allowed values are [' + ', '.join(places_to_check) + ']. Default is LibGuides.',
                        metavar='',
                        default='libguides',
                        choices=places_to_check)
    parser.add_argument('-k', '--kbart',
                        help='path to a KBART file to check.',
                        metavar='')
    parser.add_argument('-t', '--type',
                        help='type of check to run. Allowed values are [' + ', '.join(checks_to_do) + ']. Default is text (check EZProxy by known unique text).',
                        metavar='',
                        default='text',
                        choices=checks_to_do)
    parser.add_argument('-w', '--write',
                        help='write results to file.',
                        action='store_true')
    parser.add_argument('-f', '--output_file',
                        help=('Path of location to save output with name of file. '
                              'Default is users HOME directory as check_ezproxy.txt.'),
                        default=os.path.join(os.path.expanduser('~'), 'check_ezproxy.txt'),
                        metavar='')
    parser.add_argument('-p', '--proxy',
                        help='force the presence or absence of a proxy prefix. '
                             'Without the tool will try to determine which urls to proxy. '
                             'Acceptable values are [force, no_proxy].',
                        choices=('force', 'no_proxy'),
                        metavar='')
    parser.add_argument('-c', '--config-file',
                        help='full path to a JSON file containing necessary config.',
                        metavar='')
    parser.add_argument('-s', '--save-config',
                        help='for use with -c option. Saves the configuration '
                             'file passed in so you don\'t have to keep passing it.',
                        action='store_true')
    parser.add_argument('--flush-config',
                        help='flush out any saved config. Will only get rid of '
                             'configs imported from JSON, you have to edit '
                             'Python-based config directly. Can be used in same '
                             'command with a new config.',
                        action='store_true')
    return parser
