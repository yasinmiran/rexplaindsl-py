from unittest import TestCase

from rexplaindsl.dsl.char_classes import anything, negated, union, word, intersection, simple_set_str, \
    include_unicode_script, empty_set, ranged_set_str, ranged_set_cp, simple_set_cp, lowercase, uppercase, ascii, \
    ascii_extended, alphabetic, digit, not_digit, alphanumeric, punctuation, graphical, printable, blank, hex_digit, \
    whitespace, not_whitespace, not_word, control, space, backslash, double_quotes, single_quote, backtick, bell, \
    horizontal_tab, linebreak, carriage_return, form_feed, vertical_tab
from rexplaindsl.unicode.unicode_script import UnicodeScript


class CharClassesTest(TestCase):

    def test_anything(self):
        self.assertEqual(".", anything().to_regex())

    def test_negated(self):
        self.assertEqual("[^.]", negated(anything()).to_regex())

    def test_union(self):
        self.assertEqual(r"[.0-9A-Z_a-z]", union(anything(), word()).to_regex())

    def test_difference(self):
        self.assertEqual(r"[.0-9A-Z_a-z]", union(anything(), word()).to_regex())

    def test_intersection(self):
        self.assertEqual(
            r"_",
            intersection(word(), simple_set_str("_")).to_regex()
        )

    def test_include_unicode_script(self):
        exp = empty_set()
        x = include_unicode_script(
            exp,
            UnicodeScript(UnicodeScript.GREEK),
            False
        ).to_regex()
        self.assertEqual(
            r"\p{Greek}",
            x,
        )

    def test_ranged_set_str(self):
        _from, _to = "🌑", "🌝"
        exp = ranged_set_str(_from, _to)
        self.assertEqual("[\\x{1f311}-\\x{1f31d}]", exp.to_regex())

    def test_ranged_set_cp(self):
        _from = 0x1f311  # 🌑
        _to = 0x1f31d  # 🌝
        exp = ranged_set_cp(_from, _to)
        self.assertEqual("[\\x{1f311}-\\x{1f31d}]", exp.to_regex())

    def test_simple_set_cp(self):
        exp = empty_set()
        self.assertEqual(
            "\\x{1f31d}",
            union(exp, simple_set_cp(0x1f31d)).to_regex()
        )

    def test_simple_set_str(self):
        exp = empty_set()
        self.assertEqual(
            "\\x{1f31d}",
            union(exp, simple_set_str("🌝")).to_regex()
        )

    def test_empty_set(self):
        self.assertEqual("", empty_set().to_regex())

    def test_lowercase(self):
        self.assertEqual("[a-z]", lowercase().to_regex())

    def test_uppercase(self):
        self.assertEqual("[A-Z]", uppercase().to_regex())

    def test_ascii(self):
        self.assertEqual("[\\x00-\\x7F]", ascii().to_regex())

    def test_ascii_extended(self):
        self.assertEqual("[\\x00-ÿ]", ascii_extended().to_regex())

    def test_alphabetic(self):
        self.assertEqual("[A-Za-z]", alphabetic().to_regex())

    def test_digit(self):
        self.assertEqual("[0-9]", digit().to_regex())

    def test_not_digit(self):
        self.assertEqual("[^0-9]", not_digit().to_regex())

    def test_alphanumeric(self):
        self.assertEqual("[0-9A-Za-z]", alphanumeric().to_regex())

    def test_punctuation(self):
        self.assertEqual(r"[!-\/:-@[-`{-~]", punctuation().to_regex())

    def test_graphical(self):
        self.assertEqual("[!-~]", graphical().to_regex())

    def test_printable(self):
        self.assertEqual("[ -~]", printable().to_regex())

    def test_blank(self):
        self.assertEqual(r"[\x09 ]", blank().to_regex())

    def test_hex_digit(self):
        self.assertEqual(r"[0-9A-Fa-f]", hex_digit().to_regex())

    def test_whitespace(self):
        self.assertEqual(r"[\x09-\x0D ]", whitespace().to_regex())

    def test_not_whitespace(self):
        self.assertEqual(r"[^\x09-\x0D ]", not_whitespace().to_regex())

    def test_word(self):
        self.assertEqual(r"[0-9A-Z_a-z]", word().to_regex())

    def test_not_word(self):
        self.assertEqual(r"[^0-9A-Z_a-z]", not_word().to_regex())

    def test_control(self):
        self.assertEqual(r"[\x00-\x1F\x7F]", control().to_regex())

    def test_space(self):
        self.assertEqual(r" ", space().to_regex())

    def test_backslash(self):
        self.assertEqual(r"\\", backslash().to_regex())

    def test_double_quotes(self):
        self.assertEqual(r'\"', double_quotes().to_regex())

    def test_single_quote(self):
        self.assertEqual(r'\'', single_quote().to_regex())

    def test_backtick(self):
        self.assertEqual(r'`', backtick().to_regex())

    def test_bell(self):
        self.assertEqual(r'\x07', bell().to_regex())

    def test_horizontal_tab(self):
        self.assertEqual(r'\x09', horizontal_tab().to_regex())

    def test_linebreak(self):
        self.assertEqual(r'\x0A', linebreak().to_regex())

    def test_vertical_tab(self):
        self.assertEqual(r'\x0B', vertical_tab().to_regex())

    def test_form_feed(self):
        self.assertEqual(r'\x0C', form_feed().to_regex())

    def test_carriage_return(self):
        self.assertEqual(r'\x0D', carriage_return().to_regex())
