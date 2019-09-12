import logging

logger = logging.getLogger('got_fleas.categorize')


def position(plist):
    logger.debug('categorizing players by position')
    grouped = {}
    for p in plist:
        if p.position not in grouped:
            grouped[p.position] = {
                'players': [p],
                'category': 'Position',
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
                'category': 'Injury Status',
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
                'category': 'Bye Week',
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
                'category': 'Team'
            }
        else:
            grouped[p.team]['players'].append(p)
    return grouped


CATEGORIES = {
    'position': position,
    'injury': injury,
    'bye': bye,
    'team': team,
}
