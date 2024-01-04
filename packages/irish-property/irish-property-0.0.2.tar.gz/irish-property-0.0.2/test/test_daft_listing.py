from unittest import TestCase

from irish_property.daft_listing import DaftListing


class ListingTest(TestCase):
    # get_media_urls
    # parse_constructed_date
    def test_parse_floor_area(self):
        class MockObj:
            def __init__(self, *args, **kwargs):
                self.floorArea = {"value": 123, "unit": "METRES_SQUARED"}

        self.assertEqual(
            DaftListing(config=None, source="unittest", _obj=None).parse_floor_area(
                MockObj()
            ),
            123.0,
        )

    def test_parse_constructed_date(self):
        class MockObj:
            def __init__(self, *args, **kwargs):
                self.dateOfConstruction = "1980"

        self.assertEqual(
            DaftListing(
                config=None, source="unittest", _obj=None
            ).parse_constructed_date(MockObj()),
            1980,
        )
