import sys
import time
import logging
import argparse
import schedule
from typing import Optional
from logging import getLogger

from .nitter_guest import NitterGuest
from .token_file_organizer import TokenFileOrganizer
from .version import get_version
from .const import PACKAGE_NAME

logger = getLogger(__name__)

def main():
    """CLI entrypoint for the nitterguest package
    """
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME, usage='nitterguest -t YOUR_ACCESS_TOKEN -o guest_accounts.json -r', description=PACKAGE_NAME + ': create nitter guest json')
    parser.add_argument('-t', '--token', help='access token', type=str, required=True)
    parser.add_argument('-o', '--output', help='output filename', type=str, required=False)
    parser.add_argument('-r', '--reload', help='Automatically reload file', action='store_true')
    parser.add_argument('-v', '--version', help='Get version', action='version', version=PACKAGE_NAME + ": v" + get_version())
    parser.add_argument('--debug', help='Show debug logs', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.WARNING)

    if args.reload:
        logger.info("reload enabled")
        schedule.every(2).days.do(_run, args.token, args.output)
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        logger.info("reload disabled")
        _run(args.token, args.output)

def _run(token: str, output: Optional[str]) -> None:
    client = NitterGuest(token)
    oauth_token = None
    try:
        oauth_token = client.get_guest_oauth_token()
    except Exception as e:
        logger.info(f"get token failed (maybe because of API limit): reason {e}")
    if output:
        token_file = TokenFileOrganizer(output)
        if oauth_token:
            token_file.add(oauth_token)
        token_file.elimination()
        token_file.write()

if __name__ == "__main__":
    main()
