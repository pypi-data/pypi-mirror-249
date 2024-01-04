#!/usr/bin/env python3.11

import argparse
import shelve
import time

import gspread

from irish_property import logger
from irish_property.utils import get_listings, add_to_spreadsheet, notify
from irish_property.settings import SHELVE_LOCATION, get_configs


def process_listing(config, listing):
    with shelve.open(SHELVE_LOCATION) as db:
        if config.NAME.value not in db:
            db[config.NAME.value] = []

        if listing.address not in db[config.NAME.value]:
            logger.info(f"{config.NAME.value} | {listing.address} - {listing.url}")
            notify(
                config.NTFY_SERVER.value,
                config.NTFY_TOPIC.value,
                config.NTFY_SHORTLIST_TOPIC.value,
                listing,
            )

            if config.SPREADSHEET_ENABLED.value:
                success = False
                while not success:
                    try:
                        add_to_spreadsheet(
                            config.SPREADSHEET_NAME.value,
                            config.SPREADSHEET_EMAIL.value,
                            listing,
                        )
                    except gspread.exceptions.APIError:
                        logger.warning("gspread error, likely throttled, backing off")
                        time.sleep(30)
                    else:
                        success = True

            # append didn't work for whatever reason
            db[config.NAME.value] = db[config.NAME.value] + [listing.address]


def run():
    for config in get_configs():
        if not config.NTFY_SERVER.value:
            logger.info(f"NTFY not set up for config {config.NAME.value}, skipping")

        try:
            listings = get_listings(config)
            logger.info(f"Got {len(listings)} listings for config: {config.NAME.value}")
            for listing in listings:
                process_listing(config, listing)
        except Exception as ex:
            logger.error(f"Error processing on config {config.NAME.value}: {ex}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--once",
        dest="once",
        action="store_true",
        help="Do not endlessly loop, run once. Handy to use in your prefered service manager",
    )
    args = parser.parse_args()

    if args.once:
        run()
    else:
        while True:
            run()
            time.sleep(60 * 10)


if __name__ == "__main__":
    main()
