import logging


logger = logging.getLogger('gotfleas.league')

class Team(object):
    def __init__(self, team_id, cache, refresh=False):
        self.id = team_id
        self._cache = cache
        self._refresh = refresh

class League(object):
    def __init__(self, soup, cache, refresh=False):
        self._cache = cache
        self.refresh = refresh
        self.teams = {}
        for team in soup('div', class_='league-name'):
            team_id = team('a')[0].get('href').split('/')[-1]
            team_name = team.text
            self.teams[team_id] = team_name


def get_league(config):
    url = 'https://www.fleaflicker.com/nfl/leagues/{league}'.format(league=config.league_id)
    soup = config.cache.get_soup(url, refresh=config.refresh)
    return League(soup, config.cache, refresh=config.refresh)
