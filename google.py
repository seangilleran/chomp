# -*- coding:utf-8 -*-
""" Scraping tools for Google.

WE1S Chomp
"""

from logging import getLogger

from chomp import browser, clean


# Google & Browser Settings
GOOGLE_SEARCH_URL = 'http://google.com/search?q="{url}"+site%3A{site}&safe=off&filter=0'
GOOGLE_URL_STOPWORDS = [
    'keyword',
    'author',
    'biography',
    'contributor',
    'tag/',
    'tags/',
    'tool/',
    'forum.',
    'forums.',
    'comment/',
    'comment.',
    'comments.',
    '.pdf',
    '.docx',
    '.doc',
    '.xml',
    '/el/',
    '/es/',
    '/fr/',
    '/de/',
    '/tamil/'
]


def get_web_results(url, query, driver=None):
    """ Return all search results from a page, then move on.

    NOTE: This requires occasional human intervention to solve CAPTCHAs.
    """
    
    log = getLogger(__name__)

    url = url.rstrip('/')
    log.info('Querying "%s" using Google at: %s', query, url)

    chomp_url = GOOGLE_SEARCH_URL.format(url=url, query=query)
    while True:

        # Loop over each result candidate on the page.
        soup = browser.get_soup_from_selenium(chomp_url, driver, wait_for_captcha=True)
        for div in soup.find_all('div', {'class': 'rc'}):

            # The URL will be the first anchor tag in the div.
            link = div.find('a')
            result_url = str(link.get('href')).lower()

            # Before we go on, make sure we haven't hit a stopword.
            if next((w for w in result_url if w in GOOGLE_URL_STOPWORDS), None) is not None:
                log.info('Skipping (stopword): %s', result_url)
                continue

            # Sometimes the link's URL gets mushed in with the text. It should
            # also be cleaned of HTML symbols, just in case.
            title = clean.from_html(str(link.text).split('http')[0])

            # Parse date from result.
            # TODO: Make sure this works with relative dates.
            try:
                date = div.find('span', {'class': 'f'}).text
                date = str(date).replace(' - ', '')
                date = clean.from_datetime_str(date)
            except AttributeError:
                log.info('Skipping (no date found): %s', result_url)
                continue

            # Hand over what we have so far.
            yield dict(
                date=date,
                title=title,
                url=result_url,
                search_url=chomp_url
            )

        # Look for a "Next" link. If we can't find one, let's assume we've
        # run the well dry.
        next_link = soup.find('a', {'id': 'pnnext'})
        if next_link is not None:
            chomp_url = 'http://google.com' + str(next_link.get('href')).lower()
            continue
        break

    log.info('Finished query "%s" using WordPress API at: %s', query, url)


def get_api_results(url, query, api_key=''):
    """ Return all search results from the Google API.
    """

    pass
