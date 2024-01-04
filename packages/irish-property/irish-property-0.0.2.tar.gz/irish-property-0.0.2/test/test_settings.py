from unittest import TestCase
from mock import patch

from irish_property.constants import MYHOME_REGIONS
from irish_property.settings import get_configs


class SettingsTest(TestCase):
    @patch("os.listdir", return_value=["unittest_config.json"])
    @patch(
        "irish_property.settings.get_json",
        return_value={
            "NAME": "unittest_config",
            "BUY": True,
            "MIN_PRICE": 350000,
            "MAX_PRICE": 550000,
            "MIN_BEDS": 2,
            "MIN_METRES_SQUARED": 100,
            "NTFY_SERVER": "https://ntfy.sh",
            "NTFY_TOPIC": "unittest_config_topic",
            "USE_PROPERTY_IE": True,
            "PROPERTY_IE_COUNTY": "dublin",
            "PROPERTY_IE_AREA": "",
            "PROPERTY_IE_PROPERTY_TYPES": [
                "Detached House",
                "Semi-Detached House",
                "Apartment For Sale",
                "Bungalow For Sale",
            ],
            "USE_MYHOME": True,
            "MYHOME_REGION": "DUBLIN_SOUTH",
            "MYHOME_PROPERTY_TYPES": [
                "BUNGALOW",
                "COTTAGE",
                "COUNTRY_HOUSE",
                "DETATCHED",
                "END_TERRACE",
                "TOWNHOUSE",
            ],
            "USE_DAFT": True,
            "DAFT_LOCATIONS": ["DUBLIN_CITY"],
            "DAFT_PROPERTY_TYPES": [
                "ALL",
                "APARTMENT",
                "BUNGALOW",
                "DETACHED_HOUSE",
                "DUPLEX",
                "TERRACED_HOUSE",
                "TOWNHOUSE",
            ],
            "EXCLUDE_ADDRESS_FRAGMENTS": ["something"],
            "OLDEST_CONSTRUCTED_DATE": None,
            "MIN_IMAGES": 0,
            "MIN_BATHS": 0,
            "NTFY_SHORTLIST_TOPIC": "unittest_config_shortlist_topic",
        },
    )
    def test_get_configs_good(self, patch_get_json, patch_listdir):
        configs = list(get_configs())
        self.assertEqual(
            [d for d in dir(configs[0]) if d.isupper()],
            [
                "BUY",
                "DAFT_LOCATIONS",
                "DAFT_PROPERTY_TYPES",
                "EXCLUDE_ADDRESS_FRAGMENTS",
                "MAX_PRICE",
                "MIN_BEDS",
                "MIN_IMAGES",
                "MIN_METRES_SQUARED",
                "MIN_PRICE",
                "MYHOME_PROPERTY_TYPES",
                "MYHOME_REGION",
                "NAME",
                "NTFY_SERVER",
                "NTFY_SHORTLIST_TOPIC",
                "NTFY_TOPIC",
                "OLDEST_CONSTRUCTED_DATE",
                "PROPERTY_IE_AREA",
                "PROPERTY_IE_COUNTY",
                "PROPERTY_IE_PROPERTY_TYPES",
            ],
        )
        self.assertEqual(configs[0].MYHOME_REGION.value, 1406)

    @patch("os.listdir", return_value=[])
    def test_get_configs(self, patch_listdir):
        configs = list(get_configs())
        self.assertEqual(configs, [])
