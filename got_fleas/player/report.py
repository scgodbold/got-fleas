import logging

import got_fleas.player.categorize
import got_fleas.player.sort

from prettytable import PrettyTable


logger = logging.getLogger('gotfleas.player.report')


def players_to_strings(attrib, players):
    return [p.attr_str(attrib) for p in players]


def generate_report_table(data):
    report = PrettyTable()
    for column, values in data.items():
        report.add_column(values['title'], ['\n'.join(players_to_strings(values['sorted'], values['players']))])
    return report


def set_column_headers(data, agg_method):
    aggregators = {
        'count': len,
        'max': max,
        'min': min,
        'average': lambda x: sum(x) / len(x),
    }
    for k, v in data.items():
        try:
            agg_data = aggregators[agg_method](v['values'])
        except TypeError:
            logger.warn('attempted an unsupported aggregator {} for category {}'.format(agg_method.title(), v['category_name']))
            data[k]['title'] = v['category']
            continue
        data[k]['title'] = '{} [{:.2f}]'.format(v['category'], agg_data)


def report(report_str, players):
    # this gets me the "get" method for safe index fetching
    split_str = report_str.split('.')
    report_dict = {i: split_str[i] for i in range(len(split_str))}

    # This defines the report
    category = report_dict.get(0, None)
    if category is None:
        raise ValueError('Must supply a category to split player data into')
    sort_method = report_dict.get(1, 'rank')
    agg_method = report_dict.get(2, 'count')
    logger.debug('Generating report from player data: category - {}, sort - {}, agg - {}'.format(category, sort_method, agg_method))

    # This takes the raw player data and formats it to generate a report
    report_data = got_fleas.categorize.CATEGORIES[category.lower()](players)
    got_fleas.sort.SORT_METHODS[sort_method.lower()](report_data)
    set_column_headers(report_data, agg_method.lower())

    # This builds the physical report
    return generate_report_table(report_data)


# def create_report(query, players, league, matches, config):
#     split_query = query.split('.')
#     new_query = '.'.join(split_query[1:])

#     if split_query[0].lower() == 'players':
#         logger.debug('Found player report')
#         return player_report(new_query, players)
#     if split_query[0].lower() == 'owner':
#         logger.debug('Found owner report')
#         return owner_report(config.player_id, new_query, league, matches)
