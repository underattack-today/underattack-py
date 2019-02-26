#!/usr/bin/env python
"""
Welcome to the official module of the Underattack.Today API.
You can also use this in cli.
For more info please visit: https://portal.underattack.today/api/docs
To know about the project: https://underattack.today
"""
import argparse
import logging
import sys
from json import dumps

import requests

__author__ = "Miso Mijatovic & Matteo Neri"
__version__ = '0.1'
__email__ = "support@underattack.today"

logger = logging.getLogger(__name__)


class UnderattackAPIConnector:

    def __init__(self, user, password):
        self.base_url = 'https://portal.underattack.today/api'
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.user, self.password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @classmethod
    def perform_request(cls, method, url, *args, **kwargs):
        try:
            logger.debug('Sending request to {url}'.format(url=url,))
            response = method(url=url, *args, **kwargs)
        except requests.RequestException as error:
            logger.exception(msg='API request to {url} failed, error was {error}.'.format(url=url, error=error,))
            raise error
        else:
            return response

    def lookup_ip(self, ip):
        logger.debug('Get lookup IP for {}'.format(ip))
        response = self.perform_request(
            method=self.session.get,
            url='{}/lookup/ip/{}'.format(self.base_url, ip)
        ).json()
        return response

    def get_daily_feeds_yesterday(self):
        logger.debug(msg='Get yesterday\'s feeds')
        response = self.perform_request(
            method=self.session.get,
            url='{}/feeds/yesterday'.format(self.base_url)
        ).json()
        return response


def _configure_logging(stdout, file_name, quiet, debug):

    if file_name:
        formatter = logging.Formatter('%(asctime)s - %(levelname)10s - %(message)s')
        handler = logging.FileHandler(file_name)
    elif stdout:
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)

    if (file_name or stdout) and not quiet:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    if quiet:
        logger.disabled = True


def _parse_arguments():
    parser = argparse.ArgumentParser(description='Underattack.Today API Client. '
                                                 'Visit https://portal.underattack.today/api/docs')

    parser.add_argument('--version', '-v', action='version', version=__version__)

    group = parser.add_argument_group(title='Authentication')
    group.add_argument('--username', '-u', required=True)
    group.add_argument('--password', '-p', required=True)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--file-name', '-f', help='path of log file')
    group.add_argument('--stdout', '-s', action='store_true', help='log in stdout')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--debug', '-d', action='store_true', required=False, help='show more verbose logging')
    group.add_argument('--quiet', '-q', action='store_true', help='disable logging')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--lookup-ip', '-ip', help='get information about an IP')
    group.add_argument('--feeds-yesterday', '-fy', action='store_true', help='get yesterday\'s feeds')

    return parser.parse_args()


def main():

    arguments = _parse_arguments()
    _configure_logging(arguments.stdout, arguments.file_name, arguments.quiet, arguments.debug)
    logger.debug('Start!')

    with UnderattackAPIConnector(arguments.username, arguments.password) as api_session:

        result = {}

        if arguments.lookup_ip:
            result = api_session.lookup_ip(arguments.lookup_ip)
        elif arguments.feeds_yesterday:
            result = api_session.get_daily_feeds_yesterday()
        else:
            logger.error('You should not get here')

        print(dumps(result, indent=4, sort_keys=True))

    logger.debug('Finish!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)

