class Listing:
    def __init__(self, *args, **kwargs):
        self.config = kwargs["config"]

        self.address = kwargs.get("address", None)
        self.alt_addresses = kwargs.get("alt_addresses", [])
        self.price = kwargs.get("price", None)
        self.eircode = kwargs.get("eircode", None)
        self.property_type = kwargs.get("property_type", None)
        self.num_bathrooms = kwargs.get("num_bathrooms", None)
        self.num_bedrooms = kwargs.get("num_bedrooms", None)

        self._text_description = kwargs.get("text_description", None)
        self.features = kwargs.get("features", None)

        self.lat = kwargs.get("lat", None)
        self.lng = kwargs.get("lng", None)
        self._county = kwargs.get("county", None)

        self.m_squared = kwargs.get("m_squared", None)
        self.constructed_date = kwargs.get("constructed_date", None)
        self.media_urls = kwargs.get("media_urls", None)
        self.image_count = kwargs.get("image_count", None)
        self.ber_rating = kwargs.get("ber_rating", None)

        self.published_date = kwargs.get("published_date", None)
        self.seller = kwargs.get("seller", None)
        self.url = kwargs.get("url", None)

        self.source = kwargs["source"]

        self._obj = kwargs["_obj"]

    @property
    def data_quality(self) -> float:
        # how good the data for this listing is, based on how much complete metadata there is

        # TODO: maybe exclude the ones that take a while. description and county

        important_attrs = [
            "address",
            "ber_rating",
            "constructed_date",
            "eircode",
            "features",
            "image_count",
            "lat",
            "lng",
            "m_squared",
            "media_urls",
            "num_bathrooms",
            "num_bedrooms",
            "price",
            "property_type",
            "published_date",
            "seller",
            "url",
        ]
        good = 0
        for attr in important_attrs:
            if getattr(self, attr) is not None:
                good += 1

        return good / len(important_attrs)

    def serialize(self) -> dict:
        return {
            "address": self.address,
            "alt_addresses": self.alt_addresses,
            "price": self.price,
            "eircode": self.eircode,
            "property": self.property_type,
            "num_bathrooms": self.num_bathrooms,
            "num_bedrooms": self.num_bedrooms,
            "text_description": self.text_description,
            "features": self.features,
            "lat": self.lat,
            "lng": self.lng,
            "m_squared": self.m_squared,
            "constructed_date": self.constructed_date,
            "media_urls": self.media_urls,
            "image_count": self.image_count,
            "ber_rating": self.ber_rating,
            "published_date": self.published_date,
            "seller": self.seller,
            "url": self.url,
            "source": self.source,
        }

    @property
    def text_description(self):
        raise NotImplementedError()

    @property
    def county(self):
        raise NotImplementedError()

    @property
    def should_filter_out(self) -> bool:
        should_exclude = False
        for exclude in self.config.EXCLUDE_ADDRESS_FRAGMENTS.value:
            if exclude.lower() in self.address.lower():
                should_exclude = True

        if should_exclude:
            return True

        if (
            self.config.OLDEST_CONSTRUCTED_DATE.value is not None
            and self.constructed_date != "NA"
            and int(self.constructed_date) < self.config.OLDEST_CONSTRUCTED_DATE.value
        ):
            return True

        if self.image_count < self.config.MIN_IMAGES.value:
            return True

        if self.num_bathrooms is not None:
            if self.num_bathrooms < self.config.MIN_BATHS.value:
                return True

        if (
            self.m_squared
            and int(self.m_squared) < self.config.MIN_METRES_SQUARED.value
        ):
            return True

        return False

    @property
    def price_str(self) -> str:
        if not self.price:
            return

        if str(self.price)[0].isalpha():
            return self.price

        return f"€{self.price}"
