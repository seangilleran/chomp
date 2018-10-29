# -*- coding: utf-8 -*-
""" Common utilities for cleaning web content.

WE1S Chomp
"""

import html
import string
from datetime import datetime
from logging import getLogger

import bleach
import regex as re
from dateutil import parser as dateparser
from unidecode import unidecode


# Output & cleaning settings.
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
REGEX_STRING = r'http(.*?)\s|[^a-zA-Z0-9\s\.\,\!\"\'\-\:\;\(\)\p{Sc}]'


def from_html(dirty):
    """ Removes problem characters from an HTML string.
    """

    # Use Bleach to take a first pass at the HTML.
    clean = bleach.clean(dirty, tags=[], strip=True)

    # Get rid of leftovers (&lt;, etc).
    clean = html.unescape(clean)

    # Ideally we shouldn't need this since all the content is being handled
    # "safely," but the LexisNexis import script does it, so we'll do it too
    # in case some other part of the process is expecting ASCII-only text.
    clean = unidecode(clean)

    # This should get rid of any lingering HTML stuff. Experimental.
    clean = re.sub(re.compile(REGEX_STRING), ' ', clean)

    # Squeeze out the whitespace.
    clean = ''.join(c for c in clean if c in string.printable)
    clean = ' '.join(clean.split())
    clean = clean.replace(' .', '.')

    return clean


def from_datetime_str(dirty):
    """ Converts a datetime string to the standard WE1S format.
    """

    log = getLogger(__name__)

    try:
        return dateparser.parse(dirty).strftime(DATE_FORMAT)
    except:
        log.debug('Error parsing date: %s', dirty)
        return ''
