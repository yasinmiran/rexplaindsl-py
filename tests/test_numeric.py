from unittest import TestCase

from rexplaindsl.dsl.numeric import integer_range, leading_zero


class NumericTest(TestCase):

    def test_it_should_handle_small_integer_ranges(self):
        self.assertEqual(integer_range(1, 10).to_regex(), "(?:10|[1-9])")
        self.assertEqual(integer_range(1, 100).to_regex(), "(?:100|[1-9][0-9]|[1-9])")

    def test_it_should_handle_precise_integer_cases(self):
        regex_result = (
            "(?:2567[0-5]|256[0-6][0-9]|25[0-5][0-9]{2}|2[0-4][0-9]{3}|"
            "1[0-9]{4}|[1-9][0-9]{3}|[1-9][0-9]{2}|[1-9][0-9]|[1-9])"
        )
        self.assertEqual(integer_range(1, 25675).to_regex(), regex_result)

    def test_it_should_handle_relatively_large_integers(self):
        regex_result = (
            "(?:[1-9][0-9]{8}|[1-9][0-9]{7}|[1-9][0-9]{6}|[1-9][0-9]{5}|[1-9]"
            "[0-9]{4}|[1-9][0-9]{3}|[1-9][0-9]{2}|[1-9][0-9]|[0-9])"
        )
        expression = integer_range(0, 999_999_999)  # MAX
        self.assertEqual(expression.to_regex(), regex_result)

    def test_it_should_add_a_leading_zero_to_a_number_or_a_range(self):
        regex_result = "(?:0?(?:1[0-2]|[1-9]))"
        self.assertEqual(leading_zero(integer_range(1, 12)).to_regex(), regex_result)
