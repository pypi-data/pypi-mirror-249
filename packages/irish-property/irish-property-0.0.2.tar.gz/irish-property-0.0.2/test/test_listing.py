from enum import Enum

from unittest import TestCase

from irish_property.listing import Listing


class ListingTest(TestCase):
    def test_data_quality(self):
        self.assertEqual(
            Listing(config=None, source="unittest", _obj=None).data_quality, 0
        )
        self.assertGreater(
            Listing(
                config=None,
                source="unittest",
                _obj=None,
                image_count=1,
                ber_rating="A",
                property_type="house",
                url="https://something",
            ).data_quality,
            0.2,
        )

    def test_should_filter_out(self):
        self.assertFalse(
            Listing(
                address="123 main street",
                image_count=20,
                config=Enum(
                    "Config",
                    [
                        (
                            "EXCLUDE_ADDRESS_FRAGMENTS",
                            [
                                "badbad",
                            ],
                        ),
                        ("OLDEST_CONSTRUCTED_DATE", None),
                        ("MIN_IMAGES", 4),
                    ],
                ),
                source="unittest",
                _obj=None,
            ).should_filter_out
        )

        self.assertTrue(
            Listing(
                address="123 main street",
                image_count=2,
                config=Enum(
                    "Config",
                    [
                        (
                            "EXCLUDE_ADDRESS_FRAGMENTS",
                            [
                                "badbad",
                            ],
                        ),
                        ("OLDEST_CONSTRUCTED_DATE", None),
                        ("MIN_IMAGES", 4),
                    ],
                ),
                source="unittest",
                _obj=None,
            ).should_filter_out
        )

    def test_price_str(self):
        self.assertEqual(
            Listing(price=1000, config=None, source="unittest", _obj=None).price_str,
            "€1000",
        )
