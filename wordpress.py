# -*- coding:utf-8 -*-
""" Scraping tools for the WordPress API.

WE1S Chomp
"""

from logging import getLogger

from chomp import browser, clean


# WordPress API Settings
WP_API_URL = '/wp-json/wp/v2/'
WP_PAGES_URL = 'pages?search={query}&sentence=1'
WP_POSTS_URL = 'posts?search={query}&sentence=1'


def is_wordpress_url(url):
    """ Checks if URL has a WordPress site.

    Returns:
        bool: True if API present, False if disabled or not found.
    """

    log = getLogger(__name__)

    url = url.rstrip('/')

    log.debug('Testing for WordPress API at: %s', url)
    response = browser.get_json_from_url(url)
    if response is not None and response['namespace'] == 'wp/v2':
        log.debug('Ok!')
        return True

    log.debug('No API or bad response.')
    return False


def get_api_results(url, query):
    """ Collects articles from a WordPress site via the API.
    """

    log = getLogger(__name__)
    chomp_urls = []

    url = url.rstrip('/')
    log.info('Querying "%s" using WordPress API at: %s', query, url)
    if not is_wordpress_url(url):
        log.info('WordPress API not found, moving on.')
        return None

    # Build the query urls.
    query = query.replace(' ', '+')
    chomp_urls.append(WP_API_URL + WP_PAGES_URL.format(query=query))
    chomp_urls.append(WP_API_URL + WP_POSTS_URL.format(query=query))

    # Do scrape.
    for chomp_url in chomp_urls:
        for response in browser.get_json_from_url(chomp_url):
            
            log.debug('Collecting: %s', response['link'])

            yield dict(
                slug=response['slug'],
                date=clean.from_datetime_str(response['date']),
                title=clean.from_html(response['title']['rendered']),
                url=response['link'],
                search_url=chomp_url,
                content=clean.from_html(response['content']['rendered'])
            )

    log.info('Finished query "%s" using WordPress API at: %s', query, url)
