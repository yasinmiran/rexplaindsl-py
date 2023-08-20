from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.numeric import integer_range


class TestRange(TestCase):

    def test_it_should_return_expected_range(self):
        start = 65555
        end = 78000
        expression = ReXPlainDSL(
            integer_range(start, end)
        ).compile()
        for i in range(start, end + 1):
            self.assertTrue(expression.pattern.match(str(i)))
