import logging

logger = logging.getLogger('got_fleas.categorize')


def position(plist):
    logger.debug('categorizing players by position')
    grouped = {}
    for p in plist:
        if p.position not in grouped:
            grouped[p.position] = {
                'players': [p],
                'category_name': 'Position',
                'category_attr': 'position',
                'category': p.position,
            }
        else:
            grouped[p.position]['players'].append(p)
    return grouped


def injury(plist):
    logger.debug('categorizing players by injury status')
    grouped = {}
    for p in plist:
        if p.injury_status is None:
            continue
        if p.injury_status not in grouped:
            grouped[p.injury_status] = {
                'players': [p],
                'category_name': 'Injury',
                'category_attr': 'injury_status',
                'category': p.injury_status,
            }
        else:
            grouped[p.injury_status]['players'].append(p)
    return grouped


def bye(plist):
    logger.debug('categorizing players by bye week')
    grouped = {}
    for p in plist:
        if p.team in ['FA']:
            continue
        if p.bye_week not in grouped:
            grouped[p.bye_week] = {
                'players': [p],
                'category_name': 'Bye Week',
                'category_attr': 'bye_week',
                'category': p.bye_week,
            }
        else:
            grouped[p.bye_week]['players'].append(p)
    return grouped


def team(plist):
    logger.debug('categorizing players by team')
    grouped = {}
    for p in plist:
        if p.team not in grouped:
            grouped[p.team] = {
                'players': [p],
                'category_name': 'Team',
                'category_attr': 'team',
                'category': p.team,
            }
        else:
            grouped[p.team]['players'].append(p)
    return grouped


def fa(plist):
    logger.debug('categorizing players by free agents')
    return {
            'FA': {
                'players': [p for p in plist if p.team in ['FA']],
                'category_name': 'Free Agents',
                'cattegory_attr': 'team',
                'category': 'Free Agents',
            }

           }


def by_owner(mlist, pid):
    logger.debug('categorizing matches by owner')
    categorized = {}
    for match in mlist:
        if match
    return categorized


CATEGORIES = {
    'position': position,
    'injury': injury,
    'bye': bye,
    'team': team,
    'fa': fa,
}
