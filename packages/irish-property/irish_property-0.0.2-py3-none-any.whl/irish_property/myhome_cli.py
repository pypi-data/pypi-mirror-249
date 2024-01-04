import requests
import backoff
from dateutil import parser

from irish_property.listing import Listing


class MyHomeListing(Listing):
    def __init__(self, *args, **kwargs):
        super(MyHomeListing, self).__init__(*args, **kwargs)

    @classmethod
    def parse(cls, obj, config=None):
        bathrooms = (
            int(obj["BathString"].split(" ")[0]) if "BathString" in obj else None
        )
        bedrooms = int(obj["BedsString"].split(" ")[0]) if "BedsString" in obj else None
        price = (
            int(
                obj["PriceAsString"]
                .replace("€", "")
                .replace(",", "")
                .replace("Guide Price", "")
                .replace("AMV", "")
            )
            if "PriceAsString" in obj
            else None
        )  # TODO: regex
        alt_addresses = list(
            set([obj.get("OrderedDisplayAddress", None), obj.get("Address", None)])
        )
        url = "https://myhome.ie/" + obj["SeoUrl"]
        ber_rating = obj["BerRating"] if "BerRating" in obj else None
        listing = MyHomeListing(
            config=config,
            _obj=obj,
            alt_addresses=alt_addresses,
            source="myhome",
            address=obj["DisplayAddress"],
            price=price,
            eircode=None,
            property_type=obj.get("PropertyType", None),
            num_bathrooms=bathrooms,
            num_bedrooms=bedrooms,
            lat=obj.get("BrochureMap", {}).get("latitude", None),
            lng=obj.get("BrochureMap", {}).get(
                "longitude", None
            ),  # What about Location?
            m_squared=obj.get("SizeStringMeters", None),
            features=None,
            constructed_date=None,  # TODO
            media_urls=obj["Photos"],
            image_count=obj["PhotoCount"],
            url=url,
            ber_rating=ber_rating,
            published_date=parser.parse(obj["CreatedOnDate"]),
            seller=obj["GroupName"],
        )

        return listing

    @property
    def text_description(self) -> str:
        if self._text_description is not None:
            return self._text_description

        return None

    @property
    def county(self) -> str:
        if self._county is not None:
            return self._county

        return None


class MyHomeCli:
    @classmethod
    @backoff.on_exception(backoff.expo, Exception, max_tries=8, max_time=600)
    def get(cls, data):
        req = requests.post("https://api.myhome.ie/search", json=data)
        data = req.json()
        return data["SearchResults"]

    def search(self, config):
        results = []

        page = 0
        while True:
            page += 1

            page_size = 20

            data = {
                "ApiKey": "5f4bc74f-8d9a-41cb-ab85-a1b7cfc86622",  # TODO: figure out
                "Page": page,
                "PageSize": page_size,
                "SearchRequest": {
                    "PropertyTypeIds": config.MYHOME_PROPERTY_TYPES.value,
                    "PropertyClassIds": [1] if config.BUY.value else [3],
                    "PropertyStatusIds": [2, 12] if config.BUY.value else [11],
                    "RegionId": config.MYHOME_REGION.value,
                    "LocalityIds": [],  # TODO: figure out
                    "MinPrice": config.MIN_PRICE.value,
                    "MaxPrice": config.MAX_PRICE.value,
                    "MinBeds": config.MIN_BEDS.value,
                    "ChannelIds": [1],  # TODO: figure out  # is this always [1]?
                    "IsBoundsSearch": False,  # TODO: figure out
                    "Radius": {},  # TODO: figure out
                    "Polygons": [],  # TODO: figure out
                },
            }

            req_results = MyHomeCli.get(data)

            for result in req_results:
                listing = MyHomeListing.parse(result, config=config)

                results.append(listing)

            if len(req_results) < page_size:
                break

        return results
