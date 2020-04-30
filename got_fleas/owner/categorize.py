import logging


logger = logging.getLogger('gotfleas.owner.categorize')


def head2head(mlist, player_id):
    logger.debug('Categorizing matches by owner')
    owners = {}
    for match in mlist:
        # Get other owners ID
        opp = match.home_team if match.home_team != player_id else match.away_team
        opp_score, player_score = (match.home_score, match.away_score) if match.home_team != player_id else (match.away_score, match.home_score)

        if opp not in owners:
            owners[opp] = {
                'matches': [],
                'wins': 0,
                'loses': 0,
                'ties': 0,
                'points_for': 0,
                'points_against': 0,
            }
        owners[opp]['matches'].append(match)
        if match.tie:
            owners[opp]['ties'] += 1
        elif match.winner == player_id:
            owners[opp]['wins'] += 1
        else:
            owners[opp]['loses'] += 1

        owners[opp]['points_for'] += player_score
        owners[opp]['points_against'] += player_score

    return owners
