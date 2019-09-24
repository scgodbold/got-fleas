import datetime
import logging


logger = logging.getLogger('gotfleas.match')


class Match(object):
    def __init__(self, home_soup, away_soup, matchup_week):
        home_string = (home_soup('div', class_='league-name')[0].find('a').get('href')).split('/')[-1]
        self.home_team = home_string if '?' not in home_string else home_string.split('?')[0]
        away_string = (away_soup('div', class_='league-name')[0].find('a').get('href')).split('/')[-1]
        self.away_team = away_string if '?' not in away_string else away_string.split('?')[0]
        self.match_week = matchup_week
        self.home_score = home_soup('td', class_='right')[0].text
        self.away_score = away_soup('td', class_='right')[0].text

    @property
    def tie(self):
        return self.home_score == self.away_score

    @property
    def winner(self):
        return self.home_team if self.home_score > self.away_score else self.away_team

    def __repr__(self):
        return '{} [{}] v. {} [{}]'.format(self.home_team,
                                           self.home_score,
                                           self.away_team,
                                           self.away_score)


def split_matches(soup, matchup_week):
    # check if already happened
    if len(soup('thead')[0]('th')) > 2:
        return []
    matches = []
    ready = False
    home = None
    away = None
    for score in soup('tr', class_='scoreboard'):
        if ready:
            away = score
            ready = False
            matches.append(Match(home, away, matchup_week))
        else:
            home = score
            ready = True
    return matches


def get_matches(config):
    current_year = datetime.date.today().year
    matches = []
    for year in range(config.start_year, current_year + 1):
        for week in range(1, 17):
            matchup_week = '{}-{}'.format(year, week)
            url = 'https://www.fleaflicker.com/nfl/leagues/{}/scores?week={}&season={}'.format(config.league_id, week, year)
            soup = config.cache.get_soup(url)
            new_matches = split_matches(soup, matchup_week)
            if new_matches == []:
                break
            matches += new_matches
        if new_matches == []:
            break
    return matches
