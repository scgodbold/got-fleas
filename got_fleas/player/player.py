import datetime
import logging

logger = logging.getLogger('gotfleas.player')


class Player(object):

    def __init__(self, soup, cache, refresh=False):
        self._refresh = refresh
        self._cache_ref = cache

        self.name = None
        self.position = None
        self.position_rank = None
        self.overall_rank = None
        self.age = None
        self.own_percent = None
        self.draft_year = None
        self.injury_status = None
        self.ir_eligible = False

        # Parse the player box directly
        player_info = soup.find('div', class_='player')
        self.name = player_info.find('div', attrs={'class': 'player-name'}).find('a', class_='player-text').text
        self.team = player_info.find('div', attrs={'class': 'player-info'}).find('span', class_='player-team').text
        self.keeper = player_info.find('div', attrs={'class': 'player-icons'}).find('i', class_='fa-thumb-tack') is not None
        if self.team not in ['FA']:
            self.bye_week = (player_info.find('div', attrs={'class': 'player-info'}).find('span', class_='player-bye').text) \
                .replace('(', '').replace(')', '')

        # Fetch the rest of the data from the player panel
        self._parse_player_page(player_info)

        # Parsing the entire block to find
        status = soup.find_all('td')[-1].text
        self.taxi = 'TAXI' == status
        self.ir = 'IR' == status
        self.taxi_eligible = self.fetch_taxi_eligability(player_info)

    def _parse_player_page(self, soup):
        targets = {
            'Position': self._set_position,
            'Rank': self._set_ranks,
            'Age': self._set_age,
            '% Own': self._set_own_percent,
            'Draft': self._set_draft_year,
            'Inj': self._set_injury,
        }
        plink = soup.find('div', attrs={'class': 'player-name'}).find('a', class_='player-text').get('href')
        psoup = self._cache_ref.get_soup('https://www.fleaflicker.com/{}'.format(plink), refresh=self._refresh)
        ppanel = psoup.find('dl', attrs={'class': 'panel-body'})
        current_target = None
        for child in ppanel.children:
            if child.name == 'dt':
                current_target = child.text
                logger.debug('Setting player target to {}'.format(current_target))
            if child.name == 'dd' and current_target in targets:
                targets[current_target](child)

    def _set_ranks(self, soup):
        rank_text = soup.text
        self.position_rank = int(rank_text.split('-')[0])
        logger.debug('Set position rank for {} to: {}'.format(self.name, self.position_rank))
        self.overall_rank = int(rank_text.split('-')[1])
        logger.debug('Set over rank for {} to: {}'.format(self.name, self.overall_rank))

    def _set_position(self, soup):
        self.position = soup.text
        if self.position in ['S', 'CB']:
            self.position = 'DB'  # I only care about the position they play at in fantasy
        logger.debug('Set position for {} to: {}'.format(self.name, self.position))

    def _set_age(self, soup):
        self.age = int(soup.text.split('\xa0')[0])
        logger.debug('Set age for {} to: {}'.format(self.name, self.age))

    def _set_own_percent(self, soup):
        self.own_percent = int(soup.text.replace('%', ''))
        logger.debug('Set owned percent for {} to: {}'.format(self.name, self.own_percent))

    def _set_draft_year(self, soup):
        self.draft_year = int(soup.text.split(',')[0])
        logger.debug('Set draft year for {} to: {}'.format(self.name, self.draft_year))

    def _set_injury(self, soup):
        injury_text = soup.text
        self.injury_status = injury_text.split(':')[0]
        self.ir_eligible = 'IR eligible' in injury_text
        logger.debug('Set draft year for {} to: {}'.format(self.name, self.draft_year))

    def fetch_taxi_eligability(self, soup):
        # This is rough, misses undrafted free agents on second year in the league. Still better than nothing
        # Rookie always eligible
        if soup.find('div', attrs={'class': 'player-icons'}).find('i', class_='fa-graduation-cap') is not None:
            return True
        # 2nd year also eligable
        plink = soup.find('div', attrs={'class': 'player-name'}).find('a', class_='player-text').get('href')
        psoup = self._cache_ref.get_soup('https://www.fleaflicker.com/{}'.format(plink), refresh=self._refresh)
        pinfo = psoup.find('dl', attrs={'class': 'panel-body'})

        draft_info = pinfo.find('strong')
        if draft_info is None:
            return False
        year = draft_info.find_parent('dd').text.split(',')[0]
        if str(int(datetime.date.today().year) - 1) == year:
            return True
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{}({}{})'.format(self.name, self.position, self.state())

    def attr_str(self, attr):
        attrib_val = self.__dict__.get(attr)
        if attrib_val is None:
            return self.name
        return '{} [{}]'.format(self.name, attrib_val)


def get_players_by_manager(config):
    url = 'https://www.fleaflicker.com/nfl/leagues/{league}/teams/{team}'.format(league=config.league_id,
                                                                                 team=config.player_id)
    soup = config.cache.get_soup(url, refresh=config.refresh)
    players = []
    for player_soup in soup('div', class_='player'):
        players.append(Player(player_soup.find_parent('tr'), config.cache, refresh=config.refresh))
    return players
