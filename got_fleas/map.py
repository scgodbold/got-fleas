import logging


logger = logging.getLogger('got_fleas.map')


def position(players):
    position_map = {}
    for p in players:
        if p.position not in position_map:
            position_map[p.position] = [str(p)]
        else:
            position_map[p.position].append(str(p))
    return position_map


def misc(players):
    misc_map = {
        'Taxi': [],
        'IR': [],
        'FA': [],
    }
    for p in players:
        if p.taxi:
            misc_map['Taxi'].append(str(p))
        if p.ir:
            misc_map['IR'].append(str(p))
        if p.team in ['FA']:
            misc_map['FA'].append(str(p))
    return misc_map


def keeper(players):
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


def bye(players):
    bye_map = {}
    for p in players:
        if p.team in ['FA']:
            continue
        if 'Week ' + p.bye_week not in bye_map:
            bye_map['Week ' + p.bye_week] = [str(p)]
        else:
            bye_map['Week ' + p.bye_week].append(str(p))
    return bye_map


def injury(players):
    injury_map = {}
    status_map = {
        'Q': 'Questionable',
        'OUT': 'Out',
        'PUP': 'Physically Unable to Play',
        'D': 'Doubtful',
        'IR': 'Injury Reserve'
    }
    for p in players:
        if p.injury_status is None:
            continue
        translated_status = status_map.get(p.injury_status, 'Other')
        if translated_status == 'Other':
            logger.warn('Unknown player injury: [{}] {}'.format(str(p), p.injury_status))
        if translated_status not in injury_map:
            injury_map[translated_status] = [str(p)]
        else:
            injury_map[translated_status].append(str(p))
    return injury_map


def taxi(players):
    taxi_map = {}
    for p in players:
        if not p.taxi_eligible:
            continue
        if p.position not in taxi_map:
            taxi_map[p.position] = [str(p)]
        else:
            taxi_map[p.position].append(str(p))
    return taxi_map


REPORTS = {
    'position': position,
    'keeper': keeper,
    'taxi': taxi,
    'injury': injury,
    'misc': misc,
}
