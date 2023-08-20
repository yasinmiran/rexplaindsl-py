from unittest import TestCase

from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.char_classes import digit, union, punctuation, word
from rexplaindsl.dsl.groups import non_capture_group, capture_group, named_capture_group
from rexplaindsl.exceptions import InvalidGroupNameException


class GroupsTest(TestCase):

    def test_it_should_create_a_non_capturing_group(self):
        ins = ReXPlainDSL(
            non_capture_group(digit())
        ).compile()
        self.assertEqual(r"(?:[0-9])", ins.expression)

    def test_it_should_create_a_capturing_group(self):
        ins = ReXPlainDSL(
            capture_group(union(digit(), punctuation()))
        ).compile()
        self.assertEqual(r"([!-@[-`{-~])", ins.expression)

    def test_it_should_create_a_named_capture_group(self):
        ins = ReXPlainDSL(
            named_capture_group("someName", union(word(), punctuation()))
        ).compile()
        self.assertEqual(r"(?P<someName>[!-~])", ins.expression)

    def test_it_should_throw_an_exception_if_the_named_capture_group_name_is_invalid(self):
        with self.assertRaises(InvalidGroupNameException):
            named_capture_group(
                "- 902 someName",
                union(word(), punctuation())
            ).to_regex()
