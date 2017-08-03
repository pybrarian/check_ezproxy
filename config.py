import os.path

cfg = {
    'path_to_home_dir': os.path.expanduser('~'),
    'ezproxy_prefix': 'YOUR EZPROXY PREFIX',
    'max_workers': 4,
    'libguides_api_url': 'API ENDPOINT FOR LIBGUIDES DATABASE LIST', # including api key
    'ezproxy_error_text': 'TEXT UNIQUE TO YOUR EZPROXY INSTANCE',
    'kb_wskey': 'A WSKEY FOR OCLC KNOWLEDGE BASE API',
    'kb_collections': ('THE KNOWLEDGE BASE COLLECTION(S) TO CHECK',), # tuple or list
}
