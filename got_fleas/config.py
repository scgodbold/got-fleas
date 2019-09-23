import logging
import os
import os.path

import got_fleas.cache


def configure(args):
    pass


class Config(object):
    def __init__(self, cli_args):
        self._config = os.path.abspath(cli_args.config_file)
        self.log_level = 'INFO'
        self.cache_location = '.fleas'  # default
        self.league_id = None
        self.player_id = None
        self.reports = None
        self.refresh = False
        self.start_year = None
        # Use these
        self.fetch_delay = 500  # ms
        self.fetch_splay = 100  # ms
        self.read_config()
        self.read_env()
        self.read_cli(cli_args)

        # Build the cache
        self.cache = got_fleas.cache.Cache(self.cache_location,
                                           fetch_delay=self.fetch_delay,
                                           fetch_splay=self.fetch_splay,
                                           )

        # Configure basic logging
        logging.basicConfig(level=logging.getLevelName(self.log_level))

    def read_config(self):
        pass

    def read_env(self):
        if os.environ.get('FLEA_LEAGUE_ID') is not None:
            self.league_id = os.environ['FLEA_LEAGUE_ID']

        if os.environ.get('FLEA_START_YEAR') is not None:
            self.start_year = int(os.environ['FLEA_START_YEAR'])

    def read_cli(self, args):
        # Eventually add CLI args for some things, these are of the highest order
        if args.player_id is not None:
            self.player_id = args.player_id
        if args.league_id is not None:
            self.player_id = args.player_id
        self.reports = args.reports

        if args.refresh_cache:
            self.refresh = True

        if args.log_level is not None:
            self.log_level = args.log_level

        if args.start_year is not None:
            self.start_year = int(args.start_year)

    def valid(self):
        if self.league_id is not None:
            return False
