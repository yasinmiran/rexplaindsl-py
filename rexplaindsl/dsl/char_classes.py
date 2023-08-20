from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.complex.set_expression import SetExpression
from rexplaindsl.exceptions import SetElementException, GenericException
from rexplaindsl.unicode.unicode_script import UnicodeScript
from rexplaindsl.utils.common import to_codepoint


def anything():
    return simple_set_str(MetaCharacters.PERIOD)


def negated(set_exp: Expression) -> Expression:
    if isinstance(set_exp, SetExpression):
        set_exp.negate()
    return set_exp


def union(exp_a: Expression, exp_b: Expression) -> Expression:
    if not isinstance(exp_a, SetExpression) or not isinstance(exp_b, SetExpression):
        raise GenericException("union only supported for set expressions")
    return exp_a.union(exp_b)


def difference(exp_a: Expression, exp_b: Expression) -> Expression:
    if not isinstance(exp_a, SetExpression) or not isinstance(exp_b, SetExpression):
        raise GenericException("difference only supported for set expressions")
    return exp_a.difference(exp_b)


def intersection(exp_a: Expression, exp_b: Expression) -> Expression:
    if not isinstance(exp_a, SetExpression) or not isinstance(exp_b, SetExpression):
        raise GenericException("intersection only supported for set expressions")
    return exp_a.intersection(exp_b)


def include_unicode_script(set_exp: Expression, usc: UnicodeScript, negate: bool) -> Expression:
    if not isinstance(set_exp, SetExpression):
        raise GenericException("include_unicode_script only supported for set expressions")
    return set_exp.with_unicode_class(usc, negate)


# Construction

def ranged_set_str(_from: str, _to: str):
    if _from is None or _to is None:
        raise ValueError("None value found in codepoints.")
    if len(_from) > 2 or len(_to) > 2:
        raise SetElementException("expected bmp or astral codepoint")
    set_expr = SetExpression(False)
    set_expr.add_range(to_codepoint(_from), to_codepoint(_to))
    return set_expr


def ranged_set_cp(codepoint_a: int, codepoint_b: int) -> Expression:
    set_expr = SetExpression(False)
    set_expr.add_range(codepoint_a, codepoint_b)
    return set_expr


def simple_set_cp(*codepoints: int) -> Expression:
    set_expr = SetExpression(False)
    for c in codepoints:
        if c is None:
            raise ValueError("None value found in codepoints.")
        set_expr.add_char(c)
    return set_expr


def simple_set_str(*characters: str) -> Expression:
    set_expr = SetExpression(False)
    for c in characters:
        if c is None or len(c) > 2:
            raise SetElementException("expected bmp or astral codepoint")
        set_expr.add_char(to_codepoint(c))
    return set_expr


def empty_set() -> Expression:
    return SetExpression(False)


# Posix

def lowercase() -> Expression:
    return ranged_set_str('a', 'z')


def uppercase() -> Expression:
    return ranged_set_str('A', 'Z')


def ascii() -> Expression:
    return ranged_set_cp(0x00, 0x7F)


def ascii_extended() -> Expression:
    return ranged_set_cp(0x00, 0xFF)


def alphabetic() -> Expression:
    return union(lowercase(), uppercase())


def digit() -> Expression:
    return ranged_set_str("0", "9")


def not_digit() -> Expression:
    return negated(digit())


def alphanumeric() -> Expression:
    return union(alphabetic(), digit())


def punctuation() -> Expression:
    elements = [char for char in r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"]
    return simple_set_str(*elements)


def graphical() -> Expression:
    return union(alphanumeric(), punctuation())


def printable() -> Expression:
    return union(graphical(), simple_set_cp(0x20))


def blank() -> Expression:
    return simple_set_cp(0x09, 0x20)


def hex_digit() -> Expression:
    return union(
        ranged_set_str("A", "F"),
        union(digit(), ranged_set_str("a", "f")),
    )


def whitespace() -> Expression:
    return simple_set_cp(0x20, 0x9, 0xA, 0xB, 0xC, 0xD)


def not_whitespace() -> Expression:
    return negated(whitespace())


def word() -> Expression:
    return union(alphanumeric(), simple_set_str("_"))


def not_word() -> Expression:
    return negated(word())


def control() -> Expression:
    return union(ranged_set_cp(0x0, 0x1F), simple_set_cp(0x7f))


# Escape Sequences

def space() -> Expression:
    return simple_set_str(" ")


def backslash() -> Expression:
    return simple_set_str("\\")


def double_quotes() -> Expression:
    return simple_set_str("\"")


def single_quote() -> Expression:
    return simple_set_str("'")


def backtick() -> Expression:
    return simple_set_str("`")


def bell() -> Expression:
    return simple_set_cp(0x07)


def horizontal_tab() -> Expression:
    return simple_set_cp(0x09)


def linebreak() -> Expression:
    return simple_set_cp(0x0A)


def vertical_tab() -> Expression:
    return simple_set_cp(0x0B)


def form_feed() -> Expression:
    return simple_set_cp(0x0C)


def carriage_return() -> Expression:
    return simple_set_cp(0x0D)
