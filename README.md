# Check for EZProxy configurations
A simple command-line script to check that EZProxy configurations exist for library databases. Currently works with LibGuides A-Z databases and OCLC Knowledge Base. Built/Tested with Python 3.4, no guarantees for older versions.

Quick Start
===========
1. Clone the repository.
2. Optional: If you want to make the file exectuable, run chmod +x filename (in a bash system; this makes it so you shouldn't have to prepend each call with python)
3. Run `python checkProxy.py -args` (or `./checkProxy.py -args` if you did step 2 above)

Arguments
=========
The script takes 3 possible arguments (none required). Other settings are controlled by constants.py.
### -u, --urlsource
***
The location to get the urls to run the check on. Current possible options are 'libguides' and 'oclc'.

`-u libguides` will scrape your LibGuides AZ list and return the database links (only works with the default A-Z provided in LibGuides 2.0).
#### What to set in contstants.py
1. LIBGUIDES_URL - the base-url for your institutions LibGuides
2. LIBGUIDES_AZ_URL - url to LibGuides Databases A-Z page

`-u oclc` will pull links from the OCLC Knowledge Base API. You must get a WSKey from OCLC for your Knowledge Base (make sure you get a production key, not a sandbox key).
#### What to set in constants.py
1. KB_KEY - Production WSKey for OCLC Knowledge Base API
2. KB_COLLECTION - CollectionID for a knowledge base collection

### -t, --type
***
The type of check to run. Current supported checks are 'text' and 'screenshot'.

`-t text` will make a call to retrieve the page through the proxy server and compare the text returned to known error text (can't use status codes because those are 200 even for a wronly configured database). At Westfield this text is 'your EZproxy administrator must first' but you will need to set comparison text for your institution as ERROR_TEXT in constants.py
####What to set in constants.py
1. ERROR_TEXT - known text when a url is not configured for EZPRoxy

`-t screenshot` requires you install PhantomJS and have it available in your PATH (you can run `phantomjs` from the command line). It will open a browser and take a screenshot of each page.
####What to set in constants.py
1. SCREENSHOT_LOCATION - A Location relative to your home directory to save screenshots.

### -w, --write
***
Write the output to a file rather than printing to the terminal (only compatible with `-t text` because `-t screenshot` already writes results to disk)

Add New Url Sources or types of checks
======================================
import the 'register' decorator from registration.py.

###For a new Url source
Write a function that returns an iterable (i.e. list or tuple) of classes or named tuples with a url and name element. Named tuple can be used like so:
```python
from collections import namedtuple
Record = namedtuple('Record', 'name url')
new_record = Record('this_name', 'http://www.example.com')
new_record.name #will output 'this_name'
```
Decorate that function with the register decorator that takes what you want the argument to be called in the command line script and 'places'
```python
from registration import register

@register('getEmHere', 'places')
def getEmHere():
    return [listOfRecordNamedTuples]
```
Save that file to the same directory as the rest of the scripts, import it in check proxy, and it should automatically be available in the command line script.

###For a new type of check
Do the same thing as for a url source above, except the second argument to the decorator should be 'checks' and your function should take a database argument, run some kind of check, and return that argument.
```python
from registration import register
@register('checkEmGood', 'checks')
def checkEmGood(db):
    check(db)
    return db
```
MISCONFIGURED_DATABASES is available from constants.py if you want to keep a list of all the erroneous databases you encounter.
