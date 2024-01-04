import datetime

from irish_property.listing import Listing


class DaftListing(Listing):
    def __init__(self, *args, **kwargs):
        super(DaftListing, self).__init__(*args, **kwargs)

    @classmethod
    def get_media_urls(cls, obj) -> list:
        media_urls = []
        if "images" in obj.media:
            desired_size = max(
                [
                    k.replace("size", "").split("x")[0]
                    for k in obj.media["images"][0].keys()
                    if "x" in k
                ]
            )
            for block in obj.media["images"]:
                for key, value in block.items():
                    if not key.replace("size", "").split("x")[0] == desired_size:
                        continue
                    if "x" not in key:
                        continue
                    media_urls.append(value)
        return media_urls

    @classmethod
    def parse_floor_area(cls, obj) -> float | None:
        return (
            float(obj.floorArea["value"])
            if hasattr(obj, "floorArea") and obj.floorArea["unit"] == "METRES_SQUARED"
            else None
        )

    @classmethod
    def parse_constructed_date(cls, obj) -> int | None:
        return (
            int(obj.dateOfConstruction)
            if all([hasattr(obj, "dateOfConstruction"), obj.dateOfConstruction != "NA"])
            else None
        )

    @classmethod
    def parse(cls, obj, config=None) -> Listing:
        media_urls = DaftListing.get_media_urls(obj)

        floor_area = DaftListing.parse_floor_area(obj)
        constructed_date = DaftListing.parse_constructed_date(obj)

        ber_rating = obj.ber["rating"] if hasattr(obj, "ber") else None
        bathrooms = obj.numBathrooms if hasattr(obj, "numBathrooms") else None
        price = obj.price if hasattr(obj, "price") else None

        listing = DaftListing(
            config=config,
            _obj=obj,
            source="daft",
            address=obj.title,
            price=price,
            eircode=None,
            property_type=obj.propertyType,
            num_bathrooms=bathrooms,
            num_bedrooms=obj.numBedrooms,
            features=None,
            lat=obj.point["coordinates"][0],
            lng=obj.point["coordinates"][1],
            m_squared=floor_area,  # TODO: figure out for non metres squared
            constructed_date=constructed_date,
            media_urls=media_urls,
            image_count=obj.media["totalImages"],
            url=obj.url,
            ber_rating=ber_rating,
            published_date=datetime.datetime.utcfromtimestamp(
                int(obj.publishDate) / 1000
            ),
            seller=obj.seller,
        )

        return listing

    @property
    def text_description(self) -> str:
        if self._text_description is not None:
            return self._text_description

        return self._obj.description

    @property
    def county(self) -> str | None:
        if self._county is not None:
            return self._county

        try:
            return self._obj.county[0]
        except IndexError:
            return
