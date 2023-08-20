from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.char_classes import simple_set_str, negated, union, ranged_set_str, intersection, difference, \
    include_unicode_script
from rexplaindsl.unicode.unicode_script import UnicodeScript


class TestSetExpression(TestCase):

    def test_it_should_create_a_non_negated_character_class(self):
        ins = simple_set_str("A", "B", "D", "E", "C")
        self.assertEqual("[A-E]", ins.to_regex())

    def test_it_should_create_a_negated_character_class(self):
        ins = negated(simple_set_str("a", "b", "c", "d", "Z"))
        self.assertEqual("[^Za-d]", ins.to_regex())

    def test_it_should_create_a_simple_character_class_without_ranges(self):
        ins = simple_set_str("a", "d", "f", "h", "Z")
        self.assertEqual("[Zadfh]", ins.to_regex())

    def test_it_should_do_a_set_union_operation_on_two_sets(self):
        ins = union(ranged_set_str("A", "Z"), simple_set_str("a", "d", "f", "h", "Z"))
        self.assertEqual("[A-Zadfh]", ins.to_regex())

    def test_it_should_do_a_set_intersection_operation_on_two_sets(self):
        ins = intersection(
            union(ranged_set_str("A", "Z"), ranged_set_str("a", "z")),
            simple_set_str("d", "e", "f")
        )
        self.assertEqual("[d-f]", ins.to_regex())

    def test_it_should_do_a_difference_operation_on_two_sets(self):
        set_a = union(ranged_set_str("A", "Z"), ranged_set_str("a", "z"))
        set_b = union(ranged_set_str("M", "P"), ranged_set_str("m", "p"))
        ins = difference(set_a, set_b)
        self.assertEqual("[A-LQ-Za-lq-z]", ins.to_regex())

    def test_it_should_do_a_set_union_operation_on_inline_regex(self):
        ins = ReXPlainDSL(
            union(
                ranged_set_str("1", "3"),
                ranged_set_str("4", "6")
            )
        ).compile()
        self.assertEqual("[1-6]", ins.expression)

    def test_it_should_do_a_set_intersection_operation_on_inline_regex(self):
        ins = ReXPlainDSL(
            intersection(
                ranged_set_str("1", "3"),
                ranged_set_str("4", "6")
            )
        ).compile()
        self.assertEqual("", ins.expression)

    def test_it_should_do_a_set_difference_operation_on_inline_regex(self):
        ins = ReXPlainDSL(
            difference(
                ranged_set_str("1", "3"),
                simple_set_str("2", "4", "5", "6")
            )
        ).compile()
        self.assertEqual("[13]", ins.expression)

    def test_it_should_append_a_non_negated_unicode_classes_to_a_set_expression(self):
        ins = ReXPlainDSL(
            include_unicode_script(
                simple_set_str("-", "."),
                UnicodeScript.SINHALA, False
            )
        ).compile()
        self.assertEqual(r"[\-.\p{Sinhala}]", ins.expression)

    def test_it_should_append_a_negated_unicode_classes_to_a_set_expression(self):
        print(simple_set_str("-", ".").to_regex())
        ins = ReXPlainDSL(
            include_unicode_script(
                simple_set_str("-", "."),
                UnicodeScript.SINHALA,
                True
            )
        ).compile()
        self.assertEqual(r"[\-.\P{Sinhala}]", ins.expression)
