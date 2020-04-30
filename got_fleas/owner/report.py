import logging
import got_fleas.owner.categorize

from prettytable import PrettyTable


logger = logging.getLogger('gotfleas.owner.report')


def report(query, league, matches, config):
    # Right now this is the only supported owner query
    # String passed to allow for future expansion

    # Only matches for player in question
    filtered_matches = [x for x in matches if x.home_team == config.player_id or x.away_team == config.player_id]
    # get head 2 head records
    categorized_matches = got_fleas.owner.categorize.head2head(filtered_matches, config.player_id)
    report = PrettyTable()
    report.field_names = ['Team', 'Wins', 'Loses', 'Ties', 'Win %', 'Total', 'Points For', 'Points Against']
    for oid, data in categorized_matches.items():
        team_name = league.teams.get(oid)
        win_percent = (float(data['wins']) / len(data['matches'])) * 100
        report.add_row([team_name, data['wins'], data['loses'], data['ties'], '{:.2f}'.format(win_percent), len(data['matches']), '{:.2f}'.format(data['points_for']), '{:.2f}'.format(data['points_against'])])
    report.sortby = 'Wins'
    report.reversesort = True
    return report
