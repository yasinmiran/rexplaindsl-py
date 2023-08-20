from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters


def word_boundary() -> Expression:
    return Expression(lambda: MetaCharacters.WORD_BOUNDARY)


def non_word_boundary() -> Expression:
    return Expression(lambda: MetaCharacters.NON_WORD_BOUNDARY)


def start_of_line() -> Expression:
    return Expression(lambda: MetaCharacters.CARAT)


def end_of_line(crlf: bool = False) -> Expression:
    if crlf:
        return Expression(lambda: "\\x0D?" + MetaCharacters.DOLLAR)
    else:
        return Expression(lambda: MetaCharacters.DOLLAR)


def start_of_text() -> Expression:
    return Expression(lambda: MetaCharacters.BEGINNING_OF_TEXT)


def end_of_text() -> Expression:
    return Expression(lambda: MetaCharacters.END_OF_TEXT)


def exact_line_match(*expressions: Expression) -> Expression:
    inner_expr = ''.join(expr.to_regex() for expr in expressions)
    return Expression(lambda: MetaCharacters.CARAT + inner_expr + MetaCharacters.DOLLAR)


def exact_word_boundary(*expressions: Expression) -> Expression:
    inner_expr = ''.join(expr.to_regex() for expr in expressions)
    return Expression(lambda: MetaCharacters.WORD_BOUNDARY + inner_expr + MetaCharacters.WORD_BOUNDARY)
