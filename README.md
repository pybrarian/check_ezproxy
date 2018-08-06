##Check for EZProxy configurations


A simple command-line script to check that EZProxy configurations exist
for library databases. Built for checking LibGuides A-Z databases and
OCLC Knowledge Base, but can be easily extended. Built/Tested with
Python 3.4, but should work back to at least 2.7.

##Installation

Easiest way is:

``pip install check_ezproxy``

Or:

1. Clone the repository.

2. Optional: If you want to make the file exectuable, run ``chmod +x check_ezproxy_run.py`` (in a bash system; this makes it so you shouldn't have to prepend each call with python)

3. From the main directory, run ``python check_ezproxy_run.py -args`` (or ``./check_ezproxy_run.py -args`` if you did step 2 above)

4. Run ``python setup.py install`` to install (after this, you can just use the ``check_ezproxy``, setup makes it available everywhere)

Or use Docker:

1. Clone the repository

2. Edit the Dockerfile to fill in your information for environment variables (takes the place of editing cfg or JSON config)

3. With your Docker daimon running and from the project root, run ``docker build -t check_ezproxy .``

4. Now you can run Docker run commands with flags for this tool at the end, i.e. ``docker run check_ezproxy --urlsource=libguides``

Docker support is still fairly limited, and with the current Dockerfile you won't be able to check KBART files or use a JSON config.


##Use

Installing via pip or setup.py will make the ``check_ezproxy`` command
available globally. It is suggested you install it into a virtual
environment to:

1. not permanently pollute the global namespace in your shell

2. not pollute your base Python packages, as this utility uses some
   popular libraries and even if this tool isn't necessarily reliant on
   a particular version, another tool might be. Best to keep em
   separated.

##Configuration

Some minimal configuration is needed for the checks to be able to run,
and there are a couple of ways to supply this.

- Rename 'config\_template.py' to 'config.py' and supply the listed parameters. This is best for quick testing or if you want to extend the tool.

- Make a .json file containing the necessary config, then point the tool to it with the -c argument. You can optionally use a -s flag to save these configs so you don't need to point toward them again, but note that these will override any other configs you may try to give. You will need to use ``--flush-config`` to use another configuration.

- You can also use the package as a tool for making your own utility and provide config in your script. Details below.

Configurations to set are:

- **ezproxy_prefix**- the full prefix for your EZProxy server, protocol included
- **libguides_api_url**- The full URL to LibGuides API for database assets including your site id, API key, and asset\_type=10 as query parameters (v. 1.1 only at this  time, v. 1.2 soon)
- **ezproxy_error_text**- Some text on your page for proxied links with no stanzas set that you can be relatively sure is unique. The tool will match against this the page text to determine which links are not properly configured.
- **kb_wskey**- If you want to check links directly from the OCLC knowledge base, you will need to apply for an API key. Only the WSKey is needed here, not the secret.
- **kb_collections**- The name of the collections in the knowledge base to check. If using Python for config these can be in a tuple or list (or any iterable), if using JSON they go in an array. Even if you only have 1 to check, it needs to be in an iterable wrapper.

##Arguments


Note: none of these arguments are mandatory, though some rely on others
to be set as well.

**-u, --urlsource**

The location to get the urls to run the check on. Current possible options are 'libguides',
'oclc', and 'kbart' (will have to use -k to provide the path to the
KBART file to check. -k can be used on its own as well).


**-t, --type**

The type of check to run. Current supported checks are 'text' and
'link'.

``-t text`` will make a call to retrieve the page through the proxy
server and compare the text returned to known error text (can't use
status codes because those are 200 even for a wrongly configured
database). At Westfield this text is 'your EZproxy administrator must
first' but you will need to set comparison text for your institution as
ERROR\_TEXT in constants.py ``-t links`` will just make a head request
and check the status code.

**-k, --kbart**

The path to a kbart file to check. If using this, it is not necessary to
set a --urlsource, though it is fine to do so. The path can be relative,
absolute, or relative to your home directory (~)


**-w, --write**

Write the output to a file rather than printing to the standard output


**-f, --output-file**

The path and filename you wish to use in conjunction with the ``-w``. It
is necessary to also use ``-w``, but if you do not specify a file here
it will default to 'check\_proxy.txt' in your home directory.


**-p, --proxy**

Force the presence or absence of a proxy prefix. Acceptable values are:
- ``force``

- ``no_proxy``

``force`` will cause every link to have a proxy prefix regardless of
whether it 'should' (i.e. whether the LibGuides Database A-Z list has it
set to not be proxied)

``no_proxy`` will do the opposite and force the link to have no proxy
prefix, useful for checking for dead links which will still be dead when
proxied (and which might give false negatives if a link is dead and
proxied)


**-c, --config-file**

Use a JSON config file rather than one of the Python options for config
files. Arg just takes the path (relative, absolute, or relative to home)
of the .json file you want to use.


**-s, --save-config**

To be used in conjunction with ``-c``, will save the config file you
used so that you don't have to provide the path to it every time. This
saved config will trump everything.


**--flush-config**

Flush any saved JSON configuration and use either a Python or new JSON
configuration. Can be used on the same call as
``-c new_json_config.json``.

##Example Calls

Basic call to check link status on the OCLC Knowledge Base collection
defined in your configuration.

``check_ezproxy -u oclc -t link``

Call with a JSON config that we are saving.

``check_ezproxy --config=./config.json -s``

Check set OCLC knowledge base collection with an updated config.json (you can combine flags, but any flag that takes an argument must be the last one, and you can only have 1 of these when combining)

``check_ezproxy --flush-config -sc ./config.json``

##Add New Url Sources or types of checks


import the 'register' decorator from registration.py.

###For a new Url source

Write a function that returns an iterable (i.e. list or tuple) of
classes or named tuples with a url and name element. Named tuple can be
used like so:

```python
from collections import namedtuple
Record = namedtuple('Record', 'name url')
new_record = Record('this_name', 'http://www.example.com')
print(new_record.name)  # will output 'this_name'
```

Decorate that function with the register decorator that takes what you
want the argument to be called in the command line script and 'places'

```python
from registration import register

@register('get_links_here', 'places')
def get_links_here():
    return [list_of_record_named_tuples]
```

Save that file to the same directory as the rest of the scripts, import
it in check proxy, and it should automatically be available in the
command line script.

###For a new type of check

Do the same thing as for a url source above, except the second argument
to the decorator should be 'checks' and your function should take a
database argument and a config argument, run some kind of check, and
return that object if everything is fine and an object with name, url,
and a new status attribute if something went wrong.

```python
from registration import register
@register('check_em_good', 'checks')
def check_em_good(db):
    check(db)
    return db
```

You can also just add the check to the checks.py or places.py files and
(optionally) make a pull request to bring your checks into the main
repository.
