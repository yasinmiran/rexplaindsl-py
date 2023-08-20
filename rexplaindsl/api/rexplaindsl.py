from typing import Dict

import re2

from rexplaindsl.api.expression import Expression


class Flags:
    CASE_INSENSITIVE = 1
    DOTALL = 2
    MULTILINE = 4
    DISABLE_UNICODE_GROUPS = 8
    LONGEST_MATCH = 16

    def __init__(self, value: int) -> None:
        self.value = value


class ReXPlainDSL:

    def __init__(self, *expressions: Expression) -> None:
        self.expression = ''.join(expr.to_regex() for expr in expressions)
        self.pattern = None

    @staticmethod
    def get_matched_groups(match) -> Dict[int, str]:
        groups = {}
        for i in range(1, match.lastindex + 1):
            groups[i] = match.group(i)
        return groups

    def compile(self, *flags: Flags):
        fl = 0
        for flag in flags:
            fl |= flag.value
        self.pattern = re2.compile(self.expression, fl)
        return self

    @property
    def pattern_instance(self):
        if not self.pattern:
            raise ValueError("Pattern instance is None. Invoke compile(Flags...).")
        return self.pattern

    @property
    def regex_expression(self) -> str:
        return self.expression
