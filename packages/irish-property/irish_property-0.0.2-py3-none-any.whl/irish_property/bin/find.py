from irish_property import logger
from irish_property.utils import get_listings
from irish_property.settings import get_configs


def main():
    for config in get_configs():
        listings = get_listings(config)
        logger.info(f"Got {len(listings)} listings for config: {config.NAME.value}")
        for listing in listings:
            logger.info(
                f"{config.NAME.value} | {listing.address} | {listing.price_str} Bed {listing.num_bedrooms} Bath {listing.num_bathrooms} ㎡ {listing.m_squared}"
            )


if __name__ == "__main__":
    main()
