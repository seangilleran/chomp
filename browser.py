# -*- coding: utf-8 -*-
""" Common utilities for interacting with websites through Selenium and URLLIB.

WE1S Chomp
"""

import json
import urllib
from logging import getLogger

from bs4 import BeautifulSoup
from selenium import webdriver


def get_webdriver(grid_url):
    """ Get a handle to the Selenium webdriver or make a new one.
    """

    capabilities = webdriver.DesiredCapabilities.CHROME
    __webdriver = webdriver.Remote(
        desired_capabilities=capabilities, command_executor=grid_url)

    return __webdriver


def get_json_from_url(url):
    """ Return JSON data from a URL using URLLib.
    """

    log = getLogger(__name__)
    
    log.debug('Getting JSON from: %s', url)
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())

    except(urllib.error.HTTPError, urllib.error.URLError) as ex:
        log.debug('URLLib Error, no data collected: %s', ex)
    except(json.decoder.JSONDecodeError) as ex:
        log.warning('JSON Error, no data collected: %s', ex)
    return None


def get_soup_from_url(url):
    """ Return BeautifulSoup data from a URL using URLLib.
    """

    log = getLogger(__name__)

    log.debug('Getting BS4 from: %s', url)
    try:
        with urllib.request.urlopen(url) as response:
            return BeautifulSoup(response.read(), 'html5lib')

    except(urllib.error.HTTPError, urllib.error.URLError) as ex:
        log.debug('URLLib Error, no data collected: %s', ex)
    return None


def get_soup_from_selenium(url, driver):
    """ Return BeautifuLSoup data from a URL using Selenium.
    """

    log = getLogger(__name__)

    log.debug('Getting BS4 via Selenium from: %s', url)
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html5lib')
