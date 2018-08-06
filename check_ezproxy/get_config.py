import json
import os
import pickle

from .errors import ConfigError

try:
    from .config import cfg
except ImportError:
    pass


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


def get_env_config():
    return {
        'ezproxy_prefix': os.environ.get('EZPROXY_PREFIX'),
        'libguides_api_url': os.environ.get('LIBGUIDES_API_URL'),  # including api key
        'ezproxy_error_text': os.environ.get('EZPROXY_ERROR_TEXT'),
        'kb_wskey': os.environ.get('KB_WSKEY'),
        'kb_collections': [collection for collection in os.environ.get('KB_COLLECTIONS', '').split(',')],  # tuple or list
    }


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
    elif 'EZPROXY_PREFIX' in os.environ:
        config = get_env_config()
    else:
        try:
            config = cfg
        except NameError:
            raise ConfigError('Can not find a usable configuration. Please '
                              'check your configs or consult the documentation')
    return config
