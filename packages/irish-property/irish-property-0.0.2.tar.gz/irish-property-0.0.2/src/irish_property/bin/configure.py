import os
import json
import sys

from email_validator import validate_email, EmailNotValidError

from daft_scraper.search.options import PropertyType
from daft_scraper.search.options_location import Location

from irish_property import logger
from irish_property.constants import (
    MYHOME_REGIONS,
    MYHOME_PROPERTY_TYPES,
    PROPERTY_IE_SUB_AREAS_MAP,
    PROPERTY_IE_PROPERTY_TYPES,
)

from irish_property.settings import CONFIGS_LOCATION

DAFT_PROPERTY_TYPES_STRINGS = [d for d in dir(PropertyType) if d.isupper()]
DAFT_LOCATIONS_STRINGS = [d for d in dir(Location) if d.isupper()]
MYHOME_REGIONS_STRINGS = [d for d in dir(MYHOME_REGIONS) if d.isupper()]
MYHOME_PROPERTY_TYPES_STRINGS = [d for d in dir(MYHOME_PROPERTY_TYPES) if d.isupper()]


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


def assert_int(data, allow_blank=False):
    cleaned = data.strip().replace(",", "")
    if allow_blank and not cleaned:
        return
    if not cleaned.isnumeric():
        raise ValueError(f"Cleaned data is not numeric: {cleaned}")
    return cleaned


def get_int(message, allow_blank=False, blank_default=0):
    min_price = None
    while not min_price:
        try:
            min_price = assert_int(input(message), allow_blank=allow_blank)
        except ValueError as ex:
            logger.error(ex)
        else:
            if not min_price and allow_blank:
                return blank_default
    return int(min_price)


def main():
    os.makedirs(CONFIGS_LOCATION, exist_ok=True)

    config_names = []

    for config_filename in os.listdir(CONFIGS_LOCATION):
        config_names.append(config_filename.replace(".json", ""))
        logger.debug(
            f"Existing config: {os.path.join(CONFIGS_LOCATION, config_filename)}"
        )

    name = None
    while not name:
        name = input("Name of this config: ").strip()
        if not name:
            logger.error("Must include a name")

    if name in config_names:
        logger.warning("You are about to override an existing config")

    buy_or_rent = None
    while not buy_or_rent:
        buy_or_rent = input("Buy or rent [buy/rent]: ")
        if buy_or_rent.lower().strip() not in ["buy", "rent"]:
            logger.error("Must be one of buy or rent")
            buy_or_rent = None

    min_price = get_int("Minimum price (or blank): ", allow_blank=True, blank_default=0)
    max_price = get_int(
        "Maximum price (or blank): ", allow_blank=True, blank_default=999_999_999
    )
    if min_price > max_price:
        raise Exception("Maximum price must be greater than minimum price")

    min_beds = get_int("Minimum beds (or blank): ", allow_blank=True, blank_default=0)
    min_baths = get_int(
        "Minimum bathrooms (or blank): ", allow_blank=True, blank_default=0
    )

    min_metres_squared = get_int(
        "Minimum metres squared (or blank): ", allow_blank=True
    )

    ntfy_server = input(
        "ntfy_server (or blank if not using ntfy). Main server is https://ntfy.sh: "
    )
    ntfy_topic = input("ntfy_topic (or blank if not using ntfy): ")
    ntfy_shortlist_topic = input(
        "ntfy_topic to send shortlisted properties to (or blank if not using ntfy): "
    )

    # PROPERTY.IE

    use_property_ie = bool_yes_no("Include property.ie [y/n]: ")
    if use_property_ie:
        property_ie_county = None
        while property_ie_county is None:
            property_ie_county = input("County: ")
            if property_ie_county not in [
                c.lower() for c in PROPERTY_IE_SUB_AREAS_MAP.keys()
            ]:
                logger.error(f"Not valid: {property_ie_county}")
                property_ie_county = None

        property_ie_sub_area = None
        while property_ie_sub_area is None:
            property_ie_sub_area = input(
                "Area in county (type 'help' to print options). Blank for all: "
            )
            if property_ie_sub_area == "help":
                print(PROPERTY_IE_SUB_AREAS_MAP[property_ie_county])
                property_ie_sub_area = None
            else:
                if not property_ie_sub_area:
                    break
                if (
                    property_ie_sub_area
                    not in PROPERTY_IE_SUB_AREAS_MAP[property_ie_county]
                ):
                    logger.error(f"Not valid: {property_ie_sub_area}")
                    property_ie_sub_area = None

        property_ie_property_types = None
        while property_ie_property_types is None:
            property_ie_property_types = input(
                "Property types comma separated values (type 'help' to print options). Blank for all: "
            )
            if property_ie_property_types == "help":
                print(PROPERTY_IE_PROPERTY_TYPES)
                property_ie_property_types = None
            else:
                if not property_ie_property_types:
                    property_ie_property_types = PROPERTY_IE_PROPERTY_TYPES
                else:
                    property_ie_property_types = property_ie_property_types.split(",")
                    for value in property_ie_property_types:
                        value = value.strip()
                        if value not in PROPERTY_IE_PROPERTY_TYPES:
                            logger.error(f"Not valid: {value}")
                            property_ie_property_types = None
                            break

    # MYHOME

    use_myhome = bool_yes_no("Include myhome.ie [y/n]: ")
    if use_myhome:
        myhome_region = None
        while not myhome_region:
            myhome_region = input("MyHome region name (type 'help' to print options): ")
            if myhome_region.lower().strip() == "help":
                print(MYHOME_REGIONS_STRINGS)
                myhome_region = None
            else:
                if myhome_region not in MYHOME_REGIONS_STRINGS:
                    logger.error(f"Not valid: {myhome_region}")
                    myhome_region = None

        myhome_property_types = None
        while not myhome_property_types:
            myhome_property_types = input(
                "MyHome property types comma separated values (type 'help' to print options) Blank for all: "
            )
            if myhome_property_types.lower().strip() == "help":
                print(MYHOME_PROPERTY_TYPES_STRINGS)
                myhome_property_types = None
            else:
                if not myhome_property_types:
                    myhome_property_types = MYHOME_PROPERTY_TYPES_STRINGS
                    break
                myhome_property_types = myhome_property_types.split(",")
                for value in myhome_property_types:
                    value = value.strip()
                    if value not in MYHOME_PROPERTY_TYPES_STRINGS:
                        logger.error(f"Not valid: {value}")
                        myhome_property_types = None
                        break

    # DAFT

    use_daft = bool_yes_no("Include daft.ie [y/n]: ")
    if use_daft:
        daft_locations = None
        while not daft_locations:
            daft_locations = input(
                "Daft locations comma separated values (type 'help' to print options) Blank for all: "
            )
            if daft_locations.lower().strip() == "help":
                print(DAFT_LOCATIONS_STRINGS)
                daft_locations = None
            else:
                if not daft_locations:
                    daft_locations = DAFT_LOCATIONS_STRINGS
                else:
                    daft_locations = daft_locations.split(",")
                    for value in daft_locations:
                        value = value.strip()
                        if value not in DAFT_LOCATIONS_STRINGS:
                            logger.error(f"Not valid: {value}")
                            daft_locations = None

        daft_property_types = None
        while not daft_property_types:
            daft_property_types = input(
                "Daft property types comma separated values (type 'help' to print options) Blank for all: "
            )
            if daft_property_types.lower().strip() == "help":
                print(DAFT_PROPERTY_TYPES_STRINGS)
                daft_property_types = None
            else:
                if not daft_property_types:
                    daft_property_types = DAFT_PROPERTY_TYPES_STRINGS
                else:
                    daft_property_types = daft_property_types.split(",")
                    for value in daft_property_types:
                        value = value.strip()
                        if value not in DAFT_PROPERTY_TYPES_STRINGS:
                            logger.error(f"Not valid: {value}")
                            daft_property_types = None

    if not use_property_ie and not use_myhome and not use_daft:
        logger.error("Must use at least one of the providers")
        sys.exit()

    exclude_address_fragments = input(
        "Comma separated values of substrings that if they are in an address, the listing is ignored: "
    ).split(",")

    exclude_address_fragments = [i for i in exclude_address_fragments if i]

    spreadsheet_enabled = bool_yes_no(
        "Enable drive spreadsheet update (using gspread) [y/n]: "
    )
    if spreadsheet_enabled:
        spreadsheet_name = None
        while not spreadsheet_name:
            spreadsheet_name = input("Name of spreadsheet: ")
            if not name:
                logger.error("Must include a name")

        spreadsheet_email = None
        while not spreadsheet_email:
            spreadsheet_email = input(
                "Your email for the service account to share the spreadsheet with (leave blank if you have created the sheet and shared with the service account): "
            )
            if not spreadsheet_email:
                break

            try:
                validate_email(spreadsheet_email, check_deliverability=False)
            except EmailNotValidError:
                logger.error("Email not valid")

    with open(os.path.join(CONFIGS_LOCATION, name + ".json"), "w") as fh:
        fh.write(
            json.dumps(
                {
                    "NAME": name,
                    "BUY": buy_or_rent == "buy",
                    "MIN_PRICE": min_price,
                    "MAX_PRICE": max_price,
                    "MIN_BEDS": min_beds,
                    "MIN_BATHS": min_baths,
                    "MIN_METRES_SQUARED": min_metres_squared,
                    "NTFY_SERVER": ntfy_server,
                    "NTFY_TOPIC": ntfy_topic,
                    "NTFY_SHORTLIST_TOPIC": ntfy_shortlist_topic,
                    "USE_PROPERTY_IE": use_property_ie,
                    "PROPERTY_IE_COUNTY": property_ie_county,
                    "PROPERTY_IE_AREA": property_ie_sub_area,
                    "PROPERTY_IE_PROPERTY_TYPES": property_ie_property_types,
                    "USE_MYHOME": use_myhome,
                    "MYHOME_REGION": myhome_region,
                    "MYHOME_PROPERTY_TYPES": myhome_property_types,
                    "USE_DAFT": use_daft,
                    "DAFT_LOCATIONS": daft_locations,
                    "DAFT_PROPERTY_TYPES": daft_property_types,
                    "EXCLUDE_ADDRESS_FRAGMENTS": exclude_address_fragments,
                    "SPREADSHEET_ENABLED": spreadsheet_enabled,
                    "SPREADSHEET_NAME": spreadsheet_name,
                    "SPREADSHEET_EMAIL": spreadsheet_email,
                    "OLDEST_CONSTRUCTED_DATE": None,  # TODO
                    "MIN_IMAGES": 0,  # TODO
                }
            )
        )


if __name__ == "__main__":
    main()
