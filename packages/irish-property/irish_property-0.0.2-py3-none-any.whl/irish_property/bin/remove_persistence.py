import os
import argparse
import shelve

from irish_property import logger
from irish_property.settings import SHELVE_LOCATION


def bool_yes_no(message):
    data = input(message)
    cleaned = data.lower().strip()
    if not cleaned:
        logger.error("Invalid input, must be y or n")
        return bool_yes_no(message)
    if cleaned == "y":
        return True
    elif cleaned == "n":
        return False
    else:
        logger.error("Invalid input, must be y or n")
        return bool_yes_no(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-name",
        dest="config_name",
        help="The name of the config to remove persistence for",
    )
    args = parser.parse_args()

    if not args.config_name:
        logger.warning(
            "You selected no config name, persistence for all configs will be deleted"
        )

        confirm = bool_yes_no("Continue? [y/n]: ")
        if confirm:
            if os.path.exists(SHELVE_LOCATION):
                os.remove(SHELVE_LOCATION)
                logger.info("Persistence file deleted")
            else:
                logger.error("No persistence file to delete")
        else:
            logger.info("Close one, not deleting")
    else:
        with shelve.open(SHELVE_LOCATION) as db:
            if args.config_name not in db:
                logger.warning(f"Config {args.config_name} not found")
            else:
                db[args.config_name] = []
                logger.info(f"Config {args.config_name} persistence deleted")


if __name__ == "__main__":
    main()
