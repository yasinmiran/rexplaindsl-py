from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.unicode.unicode_script import UnicodeScript
from rexplaindsl.utils.common import as_regex_literal


def literal(literals: str) -> Expression:
    return Expression(
        lambda: as_regex_literal(literals)
    )


def quoted_literal(literals: str) -> Expression:
    return Expression(
        lambda: "".join([MetaCharacters.QUOTE_START, literals, MetaCharacters.QUOTE_END])
    )


def unicode_script_literal(script: UnicodeScript, negated: bool) -> Expression:
    block_name = script.block
    if len(block_name) == 1:
        prefix = "\\P" if negated else "\\p"
        expression = "".join([prefix, block_name])
    else:
        prefix = "\\P" + MetaCharacters.OPEN_CURLY_BRACE if negated else "\\p" + MetaCharacters.OPEN_CURLY_BRACE
        expression = "".join([prefix, block_name, MetaCharacters.CLOSE_CURLY_BRACE])
    return Expression(
        lambda: expression
    )
