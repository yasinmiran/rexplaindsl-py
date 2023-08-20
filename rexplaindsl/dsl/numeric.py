from rexplaindsl.api.expression import Expression
from rexplaindsl.complex.range_expression import RangeExpression
from rexplaindsl.dsl.char_classes import ranged_set_str
from rexplaindsl.dsl.groups import non_capture_group
from rexplaindsl.dsl.literals import literal


def leading_zero(another):
    return non_capture_group(
        Expression(
            lambda: "0?" + another.to_regex()
        )
    )


def integer_range(from_val: int, to_val: int):
    if from_val > to_val:
        raise ValueError("Integer range is out of order")
    if from_val == to_val:
        return literal(str(from_val))
    if from_val >= 0 and to_val <= 9:
        return ranged_set_str(str(from_val), str(to_val))
    return non_capture_group(RangeExpression(from_val, to_val))
