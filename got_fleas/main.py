import logging

import got_fleas.cli
import got_fleas.config
import got_fleas.league
import got_fleas.owner
import got_fleas.player


logger = logging.getLogger('got_fleas')


def main():
    args = got_fleas.cli.cli()
    config = got_fleas.config.Config(args)
    league = got_fleas.league.get_league(config)
    players = got_fleas.player.get_players_by_manager(config)
    matches = got_fleas.owner.get_matches(config)

    for report in config.reports:
        split_report = report.split('.')
        new_report = '.'.join(split_report[1:])
        if split_report[0].lower() == 'players':
            print(report + ':')
            print(got_fleas.player.report(new_report, players))
            print('')
        elif split_report[0].lower() == 'owner':
            print(report + ': ' + league.teams[config.player_id])
            print(got_fleas.owner.report(report, league, matches, config))
            print('')


if __name__ == '__main__':
    main()
