# -*- coding: utf-8 -*-
""" Common utilities for interacting with websites through Selenium and URLLIB.

WE1S Chomp
"""

import json
import urllib
from logging import getLogger
from random import uniform as rfloat
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver


# Space out requests a little bit.
SLEEP_MIN = 1.0
SLEEP_MAX = 4.0
SLEEP_SHORT = 0.2  # Pause b/w CAPTCHA check cycles.


def get_webdriver(grid_url):
    """ Get a handle to the Selenium webdriver or make a new one.
    """

    capabilities = webdriver.DesiredCapabilities.CHROME
    return webdriver.Remote(
        desired_capabilities=capabilities, command_executor=grid_url)


def get_json_from_url(url):
    """ Return JSON data from a URL using URLLib.
    """

    log = getLogger(__name__)
    json_data = None
    
    log.debug('Getting JSON from: %s', url)
    try:
        with urllib.request.urlopen(url) as response:
            json_data = json.loads(response.read())

    except(urllib.error.HTTPError, urllib.error.URLError) as ex:
        log.debug('URLLib Error, no data collected: %s', ex)
    except(json.decoder.JSONDecodeError) as ex:
        log.warning('JSON Error, no data collected: %s', ex)

    sleep(rfloat(SLEEP_MIN, SLEEP_MAX))
    return json_data


def get_soup_from_url(url):
    """ Return BeautifulSoup data from a URL using URLLib.
    """

    log = getLogger(__name__)
    soup = None

    log.debug('Getting BS4 from: %s', url)
    try:
        with urllib.request.urlopen(url) as response:
            soup = BeautifulSoup(response.read(), 'html5lib')

    except(urllib.error.HTTPError, urllib.error.URLError) as ex:
        log.debug('URLLib Error, no data collected: %s', ex)

    sleep(rfloat(SLEEP_MIN, SLEEP_MAX))
    return soup


def get_soup_from_selenium(url, driver, wait_for_captcha=False):
    """ Return BeautifulSoup data from a URL using Selenium.
    """

    log = getLogger(__name__)

    log.debug('Getting BS4 via Selenium from: %s', url)
    driver.get(url)

    # Check for CAPTCHA
    if wait_for_captcha and '/sorry/' in driver.current_url:
        log.error('CAPTCHA detected! Waiting for human...')
        while '/sorry/' in driver.current_url:
            sleep(SLEEP_SHORT)
        log.info('CAPTCHA cleared.')

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    sleep(rfloat(SLEEP_MIN, SLEEP_MAX))
    return soup
