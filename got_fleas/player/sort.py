import logging


logger = logging.getLogger('gotfleas.sort')


def rank(data):
    logger.debug('Ordering categories by position rank')
    for k, v in data.items():
        data[k]['sorted'] = 'position_rank'
        data[k]['values'] = [x.position_rank for x in v['players'] if x.position_rank is not None]
        data[k]['players'] = sorted(v['players'], key=lambda x: x.position_rank if x.position_rank is not None else 10000, reverse=False)


def bye_week(data):
    logger.debug('Ordering categories by bye week')
    for k, v in data.items():
        data[k]['sorted'] = 'bye_week'
        data[k]['values'] = [x.bye_week for x in v['players'] if x.bye_week is not None]
        data[k]['players'] = sorted(v['players'], key=lambda x: x.bye_week if x.bye_week is not None else 100, reverse=False)


def own_percent(data):
    logger.debug('Ordering categories by Owned %')
    for k, v in data.items():
        data[k]['sorted'] = 'own_percent'
        data[k]['values'] = [x.own_percent for x in v['players']]
        data[k]['players'] = sorted(v['players'], key=lambda x: x.own_percent, reverse=True)


def injury(data):
    logger.debug('Ordering categories by Injury Status')
    for k, v in data.items():
        data[k]['sorted'] = 'injury_status'
        data[k]['values'] = [x.injury_status for x in v['players'] if x.injury_status is not None]
        data[k]['players'] = sorted(v['players'], key=lambda x: x.injury_status if x.injury_status is not None else 'a', reverse=True)


def age(data):
    logger.debug('Ordering categories by Age')
    for k, v in data.items():
        data[k]['sorted'] = 'age'
        data[k]['values'] = [x.age for x in v['players']]
        data[k]['players'] = sorted(v['players'], key=lambda x: x.age, reverse=True)


SORT_METHODS = {
    'rank': rank,
    'bye': bye_week,
    'owned': own_percent,
    'injury': injury,
    'age': age,
}
