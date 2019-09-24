import argparse
import os.path


def cli():
    p = argparse.ArgumentParser()
    p.add_argument('--config-file', '-c', default=os.path.expanduser('~/.config/got_fleas.conf'), help='Defines configuration for your got_fleas tool')
    p.add_argument('--refresh-cache', '-r', action='store_true', help='Bypasses the cache and gets fresh data')
    p.add_argument('--player-id', '-p', help='Set player id to report on')
    p.add_argument('--league-id', '-l', help='Set league id to report on')
    p.add_argument('--start-year', '-y', type=int, help='Set year league started in')
    p.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    p.add_argument('reports', metavar='REPORT', type=str, nargs='+', help='Construct report strings to fetch data')
    return p.parse_args()
