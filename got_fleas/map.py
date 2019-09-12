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
    for p in players:
        if p.injury_status is None:
            continue
        if p.injury_status not in injury_map:
            injury_map[p.injury_status] = [str(p)]
        else:
            injury_map[p.injury_status].append(str(p))
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


def age(players):
    sorted_players = sorted(players, key=lambda x: x.age, reverse=False)

    age_map = {}

    for p in sorted_players:
        if p.position not in age_map:
            age_map[p.position] = ['{} ({})'.format(p.name, p.age)]
        else:
            age_map[p.position].append('{} ({})'.format(p.name, p.age))
    return age_map


def owned(players):
    sorted_players = sorted(players, key=lambda x: x.own_percent, reverse=True)
    owned_map = {}

    for p in sorted_players:
        if p.position not in owned_map:
            owned_map[p.position] = ['{} ({})'.format(p.name, p.own_percent)]
        else:
            owned_map[p.position].append('{} ({})'.format(p.name, p.own_percent))
    return owned_map


def position_rank(players):
    # Set to theoretically more players then we should care about in total, none will always be bottom
    sorted_players = sorted(players, key=lambda x: x.position_rank if x.position_rank is not None else 10000, reverse=False)
    position_map = {}

    for p in sorted_players:
        if p.position not in position_map:
            position_map[p.position] = ['{} ({})'.format(p.name, p.position_rank)]
        else:
            position_map[p.position].append('{} ({})'.format(p.name, p.position_rank))
    return position_map


REPORTS = {
    'position': position,
    'keeper': keeper,
    'taxi': taxi,
    'injury': injury,
    'misc': misc,
    'age': age,
    'owned': owned,
    'position-rank': position_rank,
}
