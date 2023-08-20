from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.dsl.groups import non_capture_group
from rexplaindsl.exceptions import QuantifierException


class GreedyQuantifier(Expression):
    pass


class ReluctantQuantifier(Expression):
    pass


def one_or_more_times(expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply + because it's already quantified")
    return GreedyQuantifier(
        lambda: non_capture_group(expression).to_regex() + MetaCharacters.PLUS
    )


def zero_or_more_times(expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply * because it's already quantified")
    return GreedyQuantifier(
        lambda: non_capture_group(expression).to_regex() + MetaCharacters.ASTERISK
    )


def exactly_or_more_times(times: int, expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply {n,} because it's already quantified")
    if times > 1000:
        raise QuantifierException("max repetition is 1000")
    if times == 0:
        return zero_or_more_times(expression)
    if times == 1:
        return one_or_more_times(expression)
    return GreedyQuantifier(
        lambda: non_capture_group(expression).to_regex() + MetaCharacters.OPEN_CURLY_BRACE + str(
            times) + MetaCharacters.COMMA + MetaCharacters.CLOSE_CURLY_BRACE
    )


def optional(expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply ? because it's already quantified")
    return GreedyQuantifier(lambda: non_capture_group(
        expression).to_regex() + MetaCharacters.QUESTION_MARK)


def exactly(times: int, expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply {n} because it's already quantified")
    if times == 0:
        raise QuantifierException("redundant sub-sequence")
    if times == 1:
        raise QuantifierException("redundant quantifier")
    if times > 1000:
        raise QuantifierException("max repetition is 1000")
    return GreedyQuantifier(lambda: non_capture_group(
        expression).to_regex() + MetaCharacters.OPEN_CURLY_BRACE + str(
        times) + MetaCharacters.CLOSE_CURLY_BRACE)


def between(m: int, n: int, expression: Expression) -> Expression:
    if isinstance(expression, (GreedyQuantifier, ReluctantQuantifier)):
        raise QuantifierException("cannot apply {m,n} because it's already quantified")
    if m > 1000 or n > 1000:
        raise QuantifierException("max repetition is {1,1000}")
    if m > n:
        raise QuantifierException("range is out of order")
    if m == 0 and n == 0:
        raise QuantifierException("redundant sub-sequence")
    if m == 0 and n == 1:
        return optional(expression)
    if m == 1 and n == 1:
        return expression
    return GreedyQuantifier(lambda: non_capture_group(
        expression).to_regex() + MetaCharacters.OPEN_CURLY_BRACE + str(
        m) + MetaCharacters.COMMA + str(n) + MetaCharacters.CLOSE_CURLY_BRACE)


def lazy(expression: Expression) -> Expression:
    if isinstance(expression, ReluctantQuantifier):
        raise QuantifierException("already marked as lazy")
    if not isinstance(expression, GreedyQuantifier):
        raise QuantifierException("must be a greedy quantifier")
    return ReluctantQuantifier(lambda: expression.to_regex() + MetaCharacters.QUESTION_MARK)
