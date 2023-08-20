from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.literals import literal, quoted_literal, unicode_script_literal
from rexplaindsl.unicode.unicode_script import UnicodeScript


class LiteralTest(TestCase):

    def test_escape_all_special_characters(self):
        ins = ReXPlainDSL(
            literal("https://swtch.com/~rsc/regexp&id=1")
        )
        self.assertEqual(r"https:\/\/swtch\.com\/~rsc\/regexp&id\=1", ins.expression)

    def test_create_strict_quote_string(self):
        ins = ReXPlainDSL(
            quoted_literal("https://swtch.com/~rsc/regexp&id=1")
        )
        self.assertEqual(r"\Qhttps://swtch.com/~rsc/regexp&id=1\E", ins.expression)

    def test_create_non_negated_unicode_script_block(self):
        ins = ReXPlainDSL(
            unicode_script_literal(UnicodeScript.SINHALA, False)
        )
        self.assertEqual(r"\p{Sinhala}", ins.expression)

    def test_create_negated_unicode_script_block(self):
        ins = ReXPlainDSL(
            unicode_script_literal(UnicodeScript.ARMENIAN, True)
        )
        self.assertEqual(r"\P{Armenian}", ins.expression)
