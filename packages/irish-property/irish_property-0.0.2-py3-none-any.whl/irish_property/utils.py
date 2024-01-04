import json
from typing import List
from enum import Enum
import urllib.parse
import cachetools.func

import requests
from thefuzz import fuzz
import gspread

from daft_scraper.search import DaftSearch, SearchType
from daft_scraper.search.options import (
    PropertyTypesOption,
    PriceOption,
    BedOption,
)
from daft_scraper.search.options_location import LocationsOption

from irish_property import logger
from irish_property.listing import Listing
from irish_property.daft_listing import DaftListing
from irish_property.myhome_cli import MyHomeCli
from irish_property.property_ie_cli import PropertyIECli


def clean_address(address: str) -> str:
    address = address.lower().strip()

    address = address.replace(",", "")
    address = address.replace(" street ", " st ")
    address = address.replace(" st. ", " st ")
    address = address.replace(" road ", " rd ")
    address = address.replace(" rd. ", " rd ")
    address = address.replace(" grove ", " gv ")
    address = address.replace(" gv. ", " gv ")
    address = address.replace(" park ", " pk ")
    address = address.replace(" pk. ", " pk ")
    address = address.replace(" avenue ", " ave ")
    address = address.replace(" ave. ", " ave ")
    address = address.replace(" square ", " sq ")
    address = address.replace(" sq. ", " sq ")
    address = address.replace(" county ", " co. ")
    address = address.replace(" co. ", " ")
    address = address.replace(" co ", " ")
    address = address.replace("ireland", "")

    if "no. " in address:
        address.replace("no. ", "")

    address = address.replace(
        "saint ", "st. "
    )  # could also be street, annoying but hey
    address = address.replace("street ", "st. ")
    address = address.replace("'s", "s")

    if address.startswith("apartment no "):
        address = address[13:]
    if address.startswith("apartment "):
        address = address[10:]
    if address.startswith("house no "):
        address = address[9:]
    if address.startswith("apt no "):
        address = address[7:]
    if address.startswith("apt. "):
        address = address[5:]
    if address.startswith("flat "):
        address = address[5:]
    if address.startswith("unit "):
        address = address[5:]
    if address.startswith("apt "):
        address = address[4:]
    if address.startswith("no "):
        address = address[3:]

    while "  " in address:
        address = address.replace("  ", " ")

    while address.startswith("0"):
        address = address[1:]

    return address.strip()


def get_myhome(config: Enum) -> List[Listing]:
    logger.info("Getting MyHome.ie results")
    clean_listings = []
    api = MyHomeCli()
    listings = api.search(config)
    for listing in listings:
        if not listing.should_filter_out:
            clean_listings.append(listing)

    return clean_listings


def get_daft(config: Enum) -> List[Listing]:
    logger.info("Getting Daft.ie results")
    clean_listings = []
    options = [  # TODO: more options, FacilitiesOption
        LocationsOption(config.DAFT_LOCATIONS.value),
        PriceOption(config.MIN_PRICE.value, config.MAX_PRICE.value),
        BedOption(config.MIN_BEDS.value, 99),
        PropertyTypesOption(config.DAFT_PROPERTY_TYPES.value),
    ]

    api = DaftSearch(SearchType.SALE if config.BUY.value else SearchType.RENT)
    listings = list(api.search(options))
    for listing in listings:
        listing = DaftListing.parse(listing, config=config)
        if not listing.should_filter_out:
            clean_listings.append(listing)

    return clean_listings


def get_property(config: Enum) -> List[Listing]:
    logger.info("Getting Property.ie results")
    clean_listings = []
    listings = PropertyIECli().search(config=config)
    for listing in listings:
        if not listing.should_filter_out:
            clean_listings.append(listing)

    return clean_listings


def is_match(orig: str, cmp: str) -> bool:
    return fuzz.partial_ratio(clean_address(orig), clean_address(cmp)) == 100


def has_matches(orig: str, cmp_lst: List[str]) -> bool:
    match_results = [
        is_match(clean_address(orig), clean_address(cmp_address))
        for cmp_address in cmp_lst
        if cmp_address
    ]
    return any([m for m in match_results])


def has_intersection_matches(orig_lst: List[Listing], cmp_lst: List[Listing]) -> bool:
    for alt_address in orig_lst:
        if alt_address is not None:
            if has_matches(alt_address, cmp_lst):
                return True
    return False


def listing_matches(listing: Listing, address_lst: List[Listing]) -> bool:
    if has_matches(listing.address, address_lst):
        return True

    if has_intersection_matches(listing.alt_addresses, address_lst):
        return True

    return False


def dedup_listings(listings: List[Listing]) -> List[Listing]:
    # TODO: allow a preference of which to keep
    #       maybe auto keep whichever has more metadata

    # also have access to secondary addresses for better deduping

    deduped_listings = []
    used_addresses = []
    for listing in listings:
        if listing_matches(listing, used_addresses):
            continue

        used_addresses.append(listing.address)
        used_addresses.extend(listing.alt_addresses)
        deduped_listings.append(listing)

    return deduped_listings


def get_listings(config: Enum) -> List[Listing]:
    clean_listings = []

    if config.USE_DAFT.value:
        clean_listings.extend(get_daft(config))
    if config.USE_MYHOME.value:
        clean_listings.extend(get_myhome(config))
    if config.USE_PROPERTY_IE.value:
        clean_listings.extend(get_property(config))

    clean_listings = sorted(clean_listings, key=lambda x: x.address)

    dedup = True
    if dedup:
        return dedup_listings(clean_listings)

    return clean_listings


@cachetools.func.ttl_cache(maxsize=128, ttl=300)
def get_sheet(name, email):
    try:
        google_service_account = gspread.service_account()
    except FileNotFoundError:
        logger.error("Cannot update spreadsheet, no service_account.json found")
    else:
        try:
            return google_service_account.open(name).sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            if not email:
                logger.error(
                    "Sheet not found, you must create the file and share it with the service account (or set an email in this config)"
                )
                raise Exception("Sheet not found")
            else:
                logger.info(f"Sheet not found, creating and sharing with {email}")

                sheet = google_service_account.create(name)
                sheet.share(email, perm_type="user", role="writer")

                return sheet.sheet1


def add_to_spreadsheet(name: str, email: str, listing: Listing):
    sheet = get_sheet(name, email)

    if not sheet.get_all_records():
        # if no data, add the headers
        sheet.append_row(
            [
                "Address",
                "Price",
                "Bedrooms",
                "Bathrooms",
                "m squared",
                "Property Type",
                "Published Date",
                "url",
            ]
        )

    sheet.append_row(
        [
            listing.address,
            listing.price,
            listing.num_bedrooms,
            listing.num_bathrooms,
            listing.m_squared,
            listing.property_type,
            str(listing.published_date),
            listing.url,
        ]
    )


def notify(server: str, topic: str, shortlist_topic: str, listing: Listing):
    url_encoded_address = urllib.parse.quote_plus(listing.address)

    message = f"{listing.price_str} Bed {listing.num_bedrooms} Bath {listing.num_bathrooms} ㎡ {listing.m_squared}"

    shortlist_body = json.dumps(
        {
            "topic": shortlist_topic,
            "message": message,
            "title": listing.address,
            "attach": listing.media_urls[0],
            "click": listing.url,
            "actions": [
                {
                    "action": "view",
                    "label": "Maps",
                    "url": f"https://www.google.com/maps/search/{url_encoded_address}",
                },
                {"action": "view", "label": "Listing", "url": listing.url},
            ],
        }
    ).replace('"', '\\"')

    requests.post(
        f"{server}/{topic}",
        data=message.encode(encoding="utf-8"),
        headers={
            "Attach": listing.media_urls[0],
            "Title": listing.address,
            "Click": listing.url,
            "Actions": f'http, Shortlist, https://ntfy.sh/, method=POST, body="{shortlist_body}";view, Maps, https://www.google.com/maps/search/{url_encoded_address};view, Listing, {listing.url}',
        },
    )
