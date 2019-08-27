#!/usr/bin/env python3
import requests
import os
from bs4 import BeautifulSoup
from prettytable import PrettyTable

URL = 'https://www.fleaflicker.com/nfl/leagues/{league}/teams/{team}'


class Player(object):
    def __init__(self, soup):
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

        if self.position in ['S', 'CB']:
            self.position = 'DB'  # I only care about the position they play at in fantasy

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


def get_player_list():
    # For MVP just fetch from environment variables
    url = URL.format(league=os.environ['FLEA_LEAGUE_ID'],
                     team=os.environ['FLEA_TEAM_ID'])
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features='html.parser')
    players = []
    for player_soup in soup('div', class_='player'):
        players.append(Player(player_soup.find_parent('tr')))
    return players


def map_to_position(players):
    position_map = {}
    for p in players:
        if p.position not in position_map:
            position_map[p.position] = [str(p)]
        else:
            position_map[p.position].append(str(p))
    return position_map


def map_to_special(players):
    special_map = {
        'Taxi': [],
        'IR': [],
        'FA': [],
    }
    for p in players:
        if p.taxi:
            special_map['Taxi'].append(str(p))
        if p.ir:
            special_map['IR'].append(str(p))
        if p.team in ['FA']:
            special_map['FA'].append(str(p))
    return special_map


def map_to_keeper(players):
    keeper_map = {
        'Cut': []
    }
    for p in players:
        if not p.keeper:
            keeper_map['Cut'].append(p.ext_player_str())
        elif p.position not in keeper_map:
            keeper_map[p.position] = [p.ext_player_str()]
        else:
            keeper_map[p.position].append(p.ext_player_str())
    return keeper_map


def map_to_bye(players):
    bye_map = {}
    for p in players:
        if p.team in ['FA']:
            continue
        if 'Week ' + p.bye_week not in bye_map:
            bye_map['Week ' + p.bye_week] = [str(p)]
        else:
            bye_map['Week ' + p.bye_week].append(str(p))
    return bye_map


def map_to_injury(players):
    injury_map = {}
    status_map = {
        'Q': 'Questionable',
        'O': 'Out',
        'IR': 'Injury Reserve'
    }
    for p in players:
        if p.injury_status is None:
            continue
        translated_status = status_map.get(p.injury_status, 'Other')
        if translated_status not in injury_map:
            injury_map[translated_status] = [str(p)]
        else:
            injury_map[translated_status].append(str(p))
    return injury_map


def print_report(pmap, title):
    report = PrettyTable()
    for column, players in pmap.items():
        header = '{} [{}]'.format(column, len(players))
        if len(players) == 0:
            report.add_column(header, ' ')  # Needs a space or everything shifts left
        else:
            report.add_column(header, ['\n'.join(players)])
    print(title + ':')
    print(report)
    print('')


def main():
    players = get_player_list()
    active_players = [x for x in players if not x.ir and not x.taxi]
    print_report(map_to_position(players), 'Position Report')
    print_report(map_to_special(players), 'Special Status Report')
    print_report(map_to_keeper(players), 'Keeper Report')
    print_report(map_to_bye(players), 'Bye Week Report')
    print_report(map_to_injury(players), 'Injury Report')

    print('Total Squad Size: {}'.format(len(players)))
    print('Active Sqaud Size: {}'.format(len(active_players)))


if __name__ == '__main__':
    main()
