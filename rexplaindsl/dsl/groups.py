from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.utils.common import as_regex_group_name


def non_capture_group(*expressions: Expression) -> Expression:
    expressions = [exp.to_regex() for exp in expressions]
    return Expression(lambda: "".join(
        [
            MetaCharacters.PAREN_OPEN,
            MetaCharacters.QUESTION_MARK,
            MetaCharacters.COLON
        ]
        + expressions +
        [MetaCharacters.PAREN_CLOSE]
    ))


def capture_group(*expressions: Expression) -> Expression:
    expressions = [exp.to_regex() for exp in expressions]
    return Expression(lambda: "".join(
        [MetaCharacters.PAREN_OPEN]
        + expressions +
        [MetaCharacters.PAREN_CLOSE]
    ))


def named_capture_group(name: str, *expressions: Expression) -> Expression:
    name = as_regex_group_name(name)
    expressions = [exp.to_regex() for exp in expressions]
    return Expression(lambda: "".join(
        [
            MetaCharacters.PAREN_OPEN,
            MetaCharacters.QUESTION_MARK,
            MetaCharacters.NAMED_CAPTURE_GROUP_PREFIX,
            MetaCharacters.LESS_THAN,
            name,
            MetaCharacters.GREATER_THAN
        ]
        + expressions +
        [MetaCharacters.PAREN_CLOSE]
    ))
