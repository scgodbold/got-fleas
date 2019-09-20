import datetime
import logging


logger = logging.getLogger('gotfleas.match')


class Match(object):
    def __init__(self, home_soup, away_soup):
        self.home_team = home_soup('div', class_='team_name')[0]('a').get('href')
        self.away_team = away_soup('div', class_='team_name')[0]('a').get('href')
        self.match_week = None
        self.home_score = home_soup('td', class_='right').text
        self.away_score = away_soup('td', class_='right').text

    @property
    def winner(self):
        return self.home_team if self.home_score > self.away_score else self.away_team

    def __repr__(self):
        return '{} [{}] v. {} [{}]'.format(self.home_team,
                                           self.home_score,
                                           self.away_team,
                                           self.away_score)


def split_matches(soup):
    # check if already happened
    if len(soup('thead')[0]('th')) > 2:
        return []
    matches = []
    ready = False
    home = None
    away = None
    for score in soup('tr', class_='scoreboard'):
        logger.warn(score)
        if ready:
            away = score
            ready = False
            matches.append(Match(home, away))
        else:
            home = score
    return matches


def get_matches(config):
    current_year = datetime.date.today().year
    matches = []
    for i in range(1, 17):
        url = 'https://www.fleaflicker.com/nfl/leagues/{}/scores?week={}&season={}'.format(config.league_id, i, current_year)
        soup = config.cache.get_soup(url)
        matches += split_matches(soup)
        logger.warn(matches)
        break
