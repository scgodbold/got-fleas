import logging

import got_fleas.cli
import got_fleas.config
import got_fleas.player
import got_fleas.league
import got_fleas.match
import got_fleas.report
import got_fleas.categorize
import got_fleas.sort


logger = logging.getLogger('got_fleas')


def main():
    args = got_fleas.cli.cli()
    config = got_fleas.config.Config(args)
    league = got_fleas.league.get_league(config)
    matches = got_fleas.match.get_matches(config)
    players = got_fleas.player.get_players_by_manager(config)

    for report in config.reports:
        print(report + ':')
        print(got_fleas.report.create_report(report, players, league, matches, config))
        print('')


if __name__ == '__main__':
    main()
