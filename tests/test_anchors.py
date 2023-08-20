from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.anchors import word_boundary, non_word_boundary, \
    start_of_line, end_of_line, start_of_text, \
    end_of_text, exact_line_match, exact_word_boundary
from rexplaindsl.dsl.char_classes import word, alphabetic
from rexplaindsl.dsl.groups import capture_group
from rexplaindsl.dsl.literals import literal
from rexplaindsl.dsl.repetition import one_or_more_times


class AnchorsTest(TestCase):

    def test_it_should_append_a_word_boundary_at_position(self):
        ins = ReXPlainDSL(
            capture_group(word_boundary(), word())
        )
        self.assertEqual(r"(\b[0-9A-Z_a-z])", ins.expression)

    def test_it_should_append_a_non_word_boundary_at_position(self):
        ins = ReXPlainDSL(
            non_word_boundary(),
            word()
        ).compile()
        self.assertEqual(r"\B[0-9A-Z_a-z]", ins.expression)

    def test_it_should_append_a_start_of_line_assertion_at_position(self):
        ins = ReXPlainDSL(
            start_of_line(),
            word()
        ).compile()
        self.assertEqual(r"^[0-9A-Z_a-z]", ins.expression)

    def test_it_should_append_end_of_line_assertion_at_position(self):
        ins = ReXPlainDSL(
            start_of_line(),
            one_or_more_times(word()),
            end_of_line(crlf=False)
        ).compile()
        self.assertEqual(r"^(?:[0-9A-Z_a-z])+$", ins.expression)

    def test_it_should_append_end_of_line_assertion_with_optional_carriage_return_at_position(self):
        ins = ReXPlainDSL(
            start_of_line(),
            one_or_more_times(word()),
            end_of_line(crlf=True)
        ).compile()
        self.assertEqual(r"^(?:[0-9A-Z_a-z])+\x0D?$", ins.expression)

    def test_it_should_append_start_of_text_assertion_at_position(self):
        ins = ReXPlainDSL(
            start_of_text(),
            word()
        ).compile()
        self.assertEqual(r"\A[0-9A-Z_a-z]", ins.expression)

    def test_it_should_append_end_of_text_assertion_at_position(self):
        ins = ReXPlainDSL(
            word(),
            end_of_text()
        ).compile()
        self.assertEqual(r"[0-9A-Z_a-z]\z", ins.expression)

    def test_it_should_wrap_the_expression_in_line_matcher(self):
        ins = ReXPlainDSL(
            exact_line_match(
                word_boundary(),
                word()
            )
        ).compile()
        self.assertEqual(r"^\b[0-9A-Z_a-z]$", ins.expression)

    def test_it_should_wrap_the_expression_in_word_boundary(self):
        ins = ReXPlainDSL(
            exact_word_boundary(
                literal("p"),
                one_or_more_times(alphabetic()),
                literal("p")
            )
        ).compile()
        self.assertEqual(r"\bp(?:[A-Za-z])+p\b", ins.expression)
