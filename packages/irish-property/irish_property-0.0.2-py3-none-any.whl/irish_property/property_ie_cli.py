import requests

import bs4

from irish_property import logger
from irish_property.listing import Listing


class PropertyListing(Listing):
    @property
    def should_prefilter_out(self) -> bool:
        should_exclude = False
        for exclude in self.config.EXCLUDE_ADDRESS_FRAGMENTS.value:
            if exclude.lower() in self.address.lower():
                should_exclude = True

        if should_exclude:
            return True

        if (
            self.config.OLDEST_CONSTRUCTED_DATE.value is not None
            and self.constructed_date
            and int(self.constructed_date) < self.config.OLDEST_CONSTRUCTED_DATE.value
        ):
            return True

        if (
            self.m_squared
            and int(self.m_squared) < self.config.MIN_METRES_SQUARED.value
        ):
            return True

        return False

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
            and self.constructed_date is not None
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

        if self.property_type not in self.config.PROPERTY_IE_PROPERTY_TYPES.value:
            return True

        return False


class PropertyIECli:
    def search(self, config=None) -> list:
        if config is None:
            return []

        results = []

        page = 0
        while True:
            page += 1

            SALE_OR_LET = "property-for-sale" if config.BUY.value else "property-to-let"

            if config.PROPERTY_IE_AREA:
                url = f"https://www.property.ie/{SALE_OR_LET}/{config.PROPERTY_IE_COUNTY.value.lower()}/{config.PROPERTY_IE_AREA.value.lower().replace(' ', '-')}/price_{config.MIN_PRICE.value}-{config.MAX_PRICE.value}/beds_{config.MIN_BEDS.value}/p_{page}"
            else:
                url = f"https://www.property.ie/{SALE_OR_LET}/{config.PROPERTY_IE_COUNTY.value.lower()}/price_{config.MIN_PRICE.value}-{config.MAX_PRICE.value}/beds_{config.MIN_BEDS.value}/p_{page}"

            req = requests.get(url)

            soup = bs4.BeautifulSoup(req.content)

            page_results = soup.find_all("div", {"class": "search_result"})

            if len(page_results) < 20:
                break

            for result in page_results:
                # TODO: parse out "Detached House" and whatever so we can filter easier. In the bed_bath section I think

                title_section = result.find("div", {"class": "sresult_address"})
                url = title_section.find("a")["href"]
                address = [i for i in title_section.text.split("\n") if i][1].strip()

                description_section = result.find(
                    "div", {"class": "sresult_description"}
                )

                price = (
                    description_section.find("h3")
                    .text.strip()
                    .replace("Region", "")
                    .replace(",", "")
                    .strip()
                    .replace("€", "")
                )
                bed_bath = description_section.find("h4").text.strip()

                property_type = bed_bath.split(", ")[-1].strip()

                num_bedrooms = None
                potential_bed_strs = [
                    i for i in bed_bath.split(", ") if "bed" in i.lower()
                ]
                if potential_bed_strs:
                    try:
                        num_bedrooms = int(
                            potential_bed_strs[0]
                            .lower()
                            .replace("bedrooms", "")
                            .replace("bedroom", "")
                            .strip()
                        )
                    except ValueError:
                        pass

                num_bathrooms = None
                potential_bath_strs = [
                    i for i in bed_bath.split(", ") if "bath" in i.lower()
                ]
                if potential_bath_strs:
                    try:
                        num_bathrooms = int(
                            potential_bath_strs[0]
                            .lower()
                            .replace("bathrooms", "")
                            .replace("bathroom", "")
                            .strip()
                        )
                    except ValueError:
                        pass

                ber_rating_url = result.find_all("img")[0]["src"]
                ber_rating = (
                    ber_rating_url.split("/")[-1]
                    .replace(".png", "")
                    .replace("ber_", "")
                )

                listing = PropertyListing(
                    config=config,
                    _obj=result,
                    alt_addresses=[],
                    source="property.ie",
                    address=address,
                    price=price,
                    eircode=None,
                    property_type=property_type,
                    num_bathrooms=num_bathrooms,
                    num_bedrooms=num_bedrooms,
                    lat=None,
                    lng=None,
                    m_squared=None,  # TODO
                    features=None,
                    constructed_date=None,  # TODO
                    media_urls=[],  # is set later
                    image_count=None,  # is set later
                    url=url,
                    ber_rating=ber_rating,
                    published_date=None,  # TODO
                    seller=None,  # TODO
                )

                if not listing.should_prefilter_out:
                    req = requests.get(listing.url)
                    soup = bs4.BeautifulSoup(req.content)

                    additional_info = soup.find(
                        "div", {"id": "searchmoreinfo_summary"}
                    ).text
                    listing.agent = additional_info[
                        additional_info.find("Agent:") + 6 : additional_info.find("PSR")
                    ].strip()

                    try:
                        photo_count_text = soup.find_all(
                            "span", {"class": "p1 pb_link"}
                        )[-1].text
                        photo_count = "1"
                        if "&" in photo_count_text:
                            photo_count = photo_count_text[
                                photo_count_text.find("&") + 2 :
                            ].split(" ")[0]
                    except:
                        try:
                            photo_count = soup.find(
                                "span", {"id": "pbxl_total_photos"}
                            ).text
                        except:
                            logger.warning(f'Could not get photo count for {listing.url}')
                            photo_count = "0"

                    listing.image_count = int(photo_count)

                    images_soup = soup.find_all("span", {"class": "pb_link"})
                    for image_soup in images_soup:
                        img = image_soup.find("img")
                        if img:
                            img_src = img.get("src", None)
                            listing.media_urls.append(img_src)

                    listing._text_description = soup.find(
                        "div", {"id": "searchmoreinfo_description"}
                    ).text

                    results.append(listing)

        return results
