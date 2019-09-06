import logging

import got_fleas.cli
import got_fleas.config
import got_fleas.map
import got_fleas.player
import got_fleas.reports


logger = logging.getLogger('got_fleas')


def main():
    args = got_fleas.cli.cli()
    config = got_fleas.config.Config(args)
    players = got_fleas.player.get_players_by_manager(config)

    for report in config.reports:
        got_fleas.reports.rprint(got_fleas.map.REPORTS[report](players), report.title())


if __name__ == '__main__':
    main()
