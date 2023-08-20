from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.char_classes import digit
from rexplaindsl.dsl.repetition import one_or_more_times, zero_or_more_times, exactly_or_more_times, optional, exactly, \
    lazy, between
from rexplaindsl.exceptions import QuantifierException


class RepetitionTest(TestCase):

    def test_it_should_append_one_or_more_times_quantifier_to_expression(self):
        ins = ReXPlainDSL(
            one_or_more_times(digit())
        ).compile()
        self.assertEqual(r"(?:[0-9])+", ins.expression)

    def test_it_should_append_zero_or_more_times_quantifier_to_expression(self):
        ins = ReXPlainDSL(
            zero_or_more_times(digit())
        ).compile()
        self.assertEqual(r"(?:[0-9])*", ins.expression)

    def test_it_should_append_exactly_or_more_times_quantifier_to_expression(self):
        ins = ReXPlainDSL(exactly_or_more_times(2, digit())).compile()
        self.assertEqual("(?:[0-9]){2,}", ins.expression)
        ins = ReXPlainDSL(exactly_or_more_times(0, digit())).compile()
        self.assertEqual("(?:[0-9])*", ins.expression)
        ins = ReXPlainDSL(exactly_or_more_times(1, digit())).compile()
        self.assertEqual("(?:[0-9])+", ins.expression)

    def test_it_should_append_optional_quantifier_to_expression(self):
        ins = ReXPlainDSL(optional(digit())).compile()
        self.assertEqual("(?:[0-9])?", ins.expression)

    def test_it_should_append_exactly_n_quantifier_to_expression(self):
        ins = ReXPlainDSL(exactly(5, digit())).compile()
        self.assertEqual("(?:[0-9]){5}", ins.expression)

    def test_it_should_append_between_quantifier_to_expression(self):
        ins = ReXPlainDSL(between(5, 10, digit())).compile()
        self.assertEqual("(?:[0-9]){5,10}", ins.expression)

    def test_it_should_append_lazy_quantifier_to_expression(self):
        ins = ReXPlainDSL(lazy(between(5, 10, digit()))).compile()
        self.assertEqual("(?:[0-9]){5,10}?", ins.expression)

    def test_it_should_not_allow_two_following_quantifiers(self):
        with self.assertRaises(QuantifierException) as context:
            zero_or_more_times(optional(digit()))
        self.assertEqual("cannot apply * because it's already quantified", str(context.exception))

        with self.assertRaises(QuantifierException) as context:
            one_or_more_times(zero_or_more_times(digit()))
        self.assertEqual("cannot apply + because it's already quantified", str(context.exception))

        with self.assertRaises(QuantifierException) as context:
            exactly_or_more_times(3, exactly(3, digit()))
        self.assertEqual("cannot apply {n,} because it's already quantified", str(context.exception))

        with self.assertRaises(QuantifierException) as context:
            optional(exactly(3, digit()))
        self.assertEqual("cannot apply ? because it's already quantified", str(context.exception))

        with self.assertRaises(QuantifierException) as context:
            between(3, 6, exactly(5, digit()))
        self.assertEqual("cannot apply {m,n} because it's already quantified", str(context.exception))

    def test_it_should_not_append_lazy_quantifier_if_greedy_quantifier_is_not_present(self):
        with self.assertRaises(QuantifierException) as context:
            lazy(digit())
        self.assertEqual("must be a greedy quantifier", str(context.exception))

    def test_it_should_not_append_lazy_quantifier_if_its_already_appended(self):
        with self.assertRaises(QuantifierException) as context:
            lazy(lazy(optional(digit())))
        self.assertEqual("already marked as lazy", str(context.exception))

    def test_it_should_not_append_lazy_quantifier_if_its_already_appended_2(self):
        with self.assertRaises(QuantifierException):
            one_or_more_times(lazy(optional(digit())))
        with self.assertRaises(QuantifierException):
            zero_or_more_times(lazy(optional(digit())))
        with self.assertRaises(QuantifierException):
            exactly_or_more_times(4, lazy(optional(digit())))
        with self.assertRaises(QuantifierException):
            optional(lazy(optional(digit())))
        with self.assertRaises(QuantifierException):
            exactly(2, lazy(optional(digit())))
        with self.assertRaises(QuantifierException):
            between(2, 4, lazy(optional(digit())))

    def test_it_should_throw_an_exception_when_exactly_quantifier_is_redundant(self):
        with self.assertRaises(QuantifierException) as context:
            ins = ReXPlainDSL(exactly(1, digit()))
            ins.compile()
        self.assertEqual("redundant quantifier", str(context.exception))

    def test_it_should_throw_an_exception_when_exactly_quantifier_applied_expression_is_redundant(self):
        with self.assertRaises(QuantifierException) as context:
            ins = ReXPlainDSL(exactly(0, digit()))
            ins.compile()
        self.assertEqual("redundant sub-sequence", str(context.exception))
