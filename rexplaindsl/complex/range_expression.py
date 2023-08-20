from collections import deque

from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters


class RangeExpression(Expression):

    def __init__(self, _r_start, _r_end):
        super().__init__(self.to_regex)
        self._rStart = _r_start
        self._rEnd = _r_end

    @staticmethod
    def left_bounds(start, end):
        result = deque()
        while start < end:
            range_instance = Range.from_start(start)
            result.append(range_instance)
            start = range_instance.end + 1
        return result

    @staticmethod
    def right_bounds(start, end):
        result = deque()
        while start < end:
            range_instance = Range.from_end(end)
            result.append(range_instance)
            end = range_instance.start - 1
        result.reverse()
        return result

    def to_regex(self):
        left = self.left_bounds(self._rStart, self._rEnd)
        last_left = left.pop()
        right = self.right_bounds(last_left.start, self._rEnd)
        first_right = right.popleft()

        merged = deque(left)
        if not last_left.overlaps(first_right):
            merged.append(last_left)
            merged.append(first_right)
        else:
            merged.append(Range.join(last_left, first_right))
        merged.extend(right)

        expression = []
        while merged:
            expression.append(merged.pop().to_regex())
            if merged:
                expression.append(MetaCharacters.ALTERNATION)

        return "".join(expression)


class Range(Expression):

    def __init__(self, start, end):
        super().__init__(self.to_regex)
        self.start = start
        self.end = end
        self.expression = []

    @classmethod
    def from_end(cls, end):
        chars = list(str(end))
        for i in range(len(chars) - 1, -1, -1):
            if chars[i] == '9':
                chars[i] = '0'
            else:
                chars[i] = '0'
                break
        return cls(int("".join(chars)), end)

    @classmethod
    def from_start(cls, start):
        chars = list(str(start))
        for i in range(len(chars) - 1, -1, -1):
            if chars[i] == '0':
                chars[i] = '9'
            else:
                chars[i] = '9'
                break
        return cls(start, int("".join(chars)))

    @staticmethod
    def join(a, b):
        return Range(a.start, b.end)

    def overlaps(self, r):
        return self.end > r.start and r.end > self.start

    def to_regex(self):
        start_str = str(self.start)
        end_str = str(self.end)
        repeated_count = 0
        previous_digit_a = '0'
        previous_digit_b = '0'

        for pos in range(len(start_str)):
            current_digit_a = start_str[pos]
            current_digit_b = end_str[pos]

            if current_digit_a == current_digit_b:
                self.expression.append(current_digit_a)
            else:
                if previous_digit_a == current_digit_a and previous_digit_b == current_digit_b:
                    repeated_count += 1
                    if pos != len(start_str) - 1:
                        continue
                    else:
                        self.expression.extend([MetaCharacters.OPEN_CURLY_BRACE, str(repeated_count + 1),
                                                MetaCharacters.CLOSE_CURLY_BRACE])
                        break
                if repeated_count > 0:
                    self.expression.extend(
                        [MetaCharacters.OPEN_CURLY_BRACE, str(repeated_count), MetaCharacters.CLOSE_CURLY_BRACE])
                    repeated_count = 0
                self.expression.extend([MetaCharacters.OPEN_SQUARE_BRACKET, current_digit_a,
                                        "" if (int(current_digit_b) - int(
                                            current_digit_a) == 1) else MetaCharacters.HYPHEN,
                                        current_digit_b, MetaCharacters.CLOSE_SQUARE_BRACKET])
                previous_digit_a = current_digit_a
                previous_digit_b = current_digit_b

        return "".join(self.expression)

    def __str__(self):
        return f"RangeGen {{ start={self.start}, end={self.end} }}"
