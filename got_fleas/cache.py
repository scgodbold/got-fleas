import datetime
import logging
import os
import os.path
import random
import requests
import time
import urllib.parse

from bs4 import BeautifulSoup


logger = logging.getLogger('got_fleas.cache')


class Cache(object):
    _date_format = '%Y.%m.%d'

    def __init__(self, location,
                 fetch_delay=0,
                 fetch_splay=0,
                 refresh_age=604800):
        self.location = os.path.abspath(location)
        self.refresh_age = refresh_age  # Defaults to 1w in seconds
        self.last_query = None
        self.fetch_delay = fetch_delay
        self.fetch_splay = fetch_splay
        if not os.path.exists(self.location):
            logger.debug('creating cache at {}'.format(self.location))
            os.makedirs(self.location)

    def get(self, url, refresh=False):
        logger.debug('Getting URL: ' + self._cache_path(url))
        c_path = self._cache_path(url)
        results = self._read_cache(c_path, refresh)
        if results is not None:
            return results

        return self._fetch_url(url, c_path)

    def get_soup(self, url, refresh=False):
        return BeautifulSoup(self.get(url, refresh=refresh), features='html.parser')

    def _cache_path(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return '{}/{}/{}'.format(self.location,
                                 parsed_url.netloc,
                                 parsed_url.path,
                                 ).replace('//', '/')

    def _read_cache(self, path, refresh):
        # If we explicitly want to refresh just bypass this
        if refresh:
            logger.debug('Refresh forced on ' + path)
            return None

        # Doesnt exist, do nothing
        if not os.path.exists('{}/age'.format(path)):
            logger.debug('No entry found for ' + path)
            return None
        if not os.path.exists('{}/content'.format(path)):
            logger.debug('Content missing for ' + path)
            return None

        # Exist check if its stale
        with open('{}/age'.format(path), 'r') as f:
            data = f.read()
        age = datetime.datetime.strptime(data, self._date_format)
        if (datetime.datetime.now() - age).total_seconds() > self.refresh_age:
            logger.debug('Expired cache entry for {}, refreshing'.format(path))
            return None

        # Not stale, return content
        with open('{}/content'.format(path), 'r') as f:
            logger.debug('Found cached version of ' + path)
            return f.read()

    def _check_delay(self):
        delay_left = self.fetch_delay - ((datetime.datetime.now() - self.last_query)/datetime.timedelta(milliseconds=1))
        if delay_left < 0:
            return

        splay = random.randint(0, self.fetch_splay)
        delay = delay_left + splay
        logger.debug('Delay was not surpassed, pausing for remainder and a random splay: {}ms'.format(str(delay)))

        time.sleep(delay/1000)  # sleep only supports seconds, but does support fractions

    def _fetch_url(self, url, path):
        if self.last_query is not None:
            self._check_delay()

        resp = requests.get(url)
        self.last_query = datetime.datetime.now()

        os.makedirs(path, exist_ok=True)
        with open('{}/content'.format(path), 'w') as f:
            f.write(resp.text)

        with open('{}/age'.format(path),  'w') as f:
            f.write(datetime.datetime.now().strftime(self._date_format))

        logger.debug('cached {} from web'.format(url))
        return resp.text
