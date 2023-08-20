from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.char_classes import digit, uppercase, lowercase, punctuation
from rexplaindsl.dsl.operators import either, either_str, concat


class OperatorsTest(TestCase):

    def test_alternation_between_multiple_expressions(self):
        ins = ReXPlainDSL(
            either(digit(), uppercase(), lowercase())
        ).compile()
        self.assertEqual(r"(?:[0-9]|[A-Z]|[a-z])", ins.expression)

    def test_alternation_between_multiple_strings(self):
        ins = ReXPlainDSL(
            either_str("http", "https", "ws", "wss")
        ).compile()
        self.assertEqual(r"(?:https?|wss?)", ins.expression)

    def test_concat_multiple_expressions_into_one(self):
        ins = ReXPlainDSL(
            concat(digit(), punctuation())
        ).compile()
        self.assertEqual(r"[0-9][!-\/:-@[-`{-~]", ins.expression)
