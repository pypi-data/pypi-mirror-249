from unittest import TestCase

from irish_property.utils import clean_address, is_match, has_matches


class UtilsTest(TestCase):
    def test_clean_address(self):
        self.assertEqual(
            clean_address("  apartment 01, main street, dublin 1"), "1 main st dublin 1"
        )

    def test_is_match(self):
        self.assertTrue(is_match("aaa", "aaa"))
        self.assertTrue(is_match("aaa", "aaab"))
        self.assertFalse(is_match("aaa", "abbb"))

    def test_has_matches(self):
        self.assertTrue(has_matches("aaa", ["aaab", "abcd"]))
        self.assertFalse(has_matches("aaa", ["bacd", "abcd"]))
