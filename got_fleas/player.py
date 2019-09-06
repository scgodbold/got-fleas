import datetime


class Player(object):

    def __init__(self, soup, cache, refresh=False):
        self._refresh = refresh
        self._cache_ref = cache
        player_info = soup.find('div', class_='player')
        self.name = player_info.find('div', attrs={'class': 'player-name'}).find('a', class_='player-text').text
        inj_status = player_info.find('div', attrs={'class': 'player-name'}).find('span', class_='injury')
        self.injury_status = inj_status.text if inj_status is not None else None
        self.position = player_info.find('div', attrs={'class': 'player-info'}).find('span', class_='position').text
        self.team = player_info.find('div', attrs={'class': 'player-info'}).find('span', class_='player-team').text
        self.keeper = player_info.find('div', attrs={'class': 'player-icons'}).find('i', class_='fa-thumb-tack') is not None

        if self.team not in ['FA']:
            self.bye_week = (player_info.find('div', attrs={'class': 'player-info'}).find('span', class_='player-bye').text) \
                .replace('(', '').replace(')', '')

        status = soup.find_all('td')[-1].text
        self.taxi = 'TAXI' == status
        self.ir = 'IR' == status
        self.taxi_eligible = self.fetch_taxi_eligability(player_info)

        if self.position in ['S', 'CB']:
            self.position = 'DB'  # I only care about the position they play at in fantasy

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

    def state(self):
        state = ''
        state = state + ' - TAXI' if self.taxi else state
        state = state + ' - IR' if self.ir else state
        state = state + ' - FA' if self.team in ['FA'] else state
        return state

    def ext_player_str(self):
        string = '{} [{}'.format(self.name, self.position)
        modifiers = []
        if self.taxi:
            modifiers.append('Taxi')
        if self.ir:
            modifiers.append('IR')
        if self.team in ['FA']:
            modifiers.append('FA')
        if len(modifiers) > 0:
            string = string + ' - ' + '|'.join(modifiers) + ']'
        else:
            string = string + ']'
        return string


def get_players_by_manager(config):
    url = 'https://www.fleaflicker.com/nfl/leagues/{league}/teams/{team}'.format(league=config.league_id,
                                                                                 team=config.player_id)
    soup = config.cache.get_soup(url, refresh=config.refresh)
    players = []
    for player_soup in soup('div', class_='player'):
        players.append(Player(player_soup.find_parent('tr'), config.cache, refresh=config.refresh))
    return players
