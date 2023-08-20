import re2

from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.dsl.literals import unicode_script_literal
from rexplaindsl.exceptions import InvalidCodepointException

SET_RESTRICTED = re2.compile(r'[\^\\\]\-"/\']')


class SetExpression(Expression):

    def __init__(self, negated=False):
        super().__init__(self.to_regex)
        self.negated = negated
        self.codepoints = set()
        self.unicodeClasses = set()

    def negate(self):
        self.negated = True

    def add_range(self, codepoint_a, codepoint_b):
        if 0x000000 <= codepoint_a <= 0X10FFFF and \
                0x000000 <= codepoint_b <= 0X10FFFF:
            if codepoint_a > codepoint_b:
                raise InvalidCodepointException("character range is out of order")
            if codepoint_a == codepoint_b:
                self.codepoints.add(codepoint_a)
                return
            self.codepoints.update(range(codepoint_a, codepoint_b + 1))
        else:
            raise InvalidCodepointException("invalid codepoint")

    def add_char(self, codepoint):
        if not (0x000000 <= codepoint <= 0X10FFFF):
            raise InvalidCodepointException("invalid codepoint")
        self.codepoints.add(codepoint)

    def union(self, b):
        if b.negated:
            self.codepoints -= b.codepoints
        else:
            self.codepoints |= b.codepoints
        return self

    def intersection(self, b):
        if b.negated:
            self.codepoints -= b.codepoints
        else:
            self.codepoints &= b.codepoints
        return self

    def difference(self, b):
        if not b.negated:
            b.negated = True
        return self.intersection(b)

    def with_unicode_class(self, block, negated):
        klass = unicode_script_literal(block, negated)
        self.unicodeClasses.add(str(klass.to_regex()))
        return self

    def to_regex(self):

        # copy the codepoints into a indexed array
        chars = sorted(list(self.codepoints))

        # return nothing if the set is empty
        if len(chars) == 0 and len(self.unicodeClasses) == 0:
            return ""

        # return only the unicode script class if it's a singleton
        if len(chars) == 0:
            if len(self.unicodeClasses) == 1 and not self.negated:
                return str(next(iter(self.unicodeClasses)))

        # avoid creating a set expression. instead just escape the sequence.
        # [a] => a (only if its not negated)
        if len(chars) == 1 and not self.negated and len(self.unicodeClasses) == 0:
            return "".join([self.to_regex_interpretable(chars[0])])

        # we use a string-builder to construct the set expression iteratively.
        expression = ""
        expression += MetaCharacters.OPEN_SQUARE_BRACKET  # open bracket
        if self.negated:
            expression += MetaCharacters.CARAT  # append carat if negated

        rangeStartIndex = -1
        isInRange = False

        curIndex = 0
        while curIndex < len(chars):
            # Check if this can be a range
            if curIndex + 1 < len(chars):
                if chars[curIndex + 1] - chars[curIndex] == 1:
                    if not isInRange:  # if this is the start
                        rangeStartIndex = curIndex
                        isInRange = True
                    curIndex += 1
                    continue
            if isInRange:
                # Check if the range is only within two characters.
                # i.e. a-b then we can simplify it to [ab]
                if curIndex - rangeStartIndex == 1:  # difference
                    expression += self.to_regex_interpretable(chars[rangeStartIndex])
                    expression += self.to_regex_interpretable(chars[curIndex])
                else:
                    expression += self.to_regex_interpretable(chars[rangeStartIndex])
                    expression += MetaCharacters.HYPHEN
                    expression += self.to_regex_interpretable(chars[curIndex])
                # Reset range starting back to initial
                rangeStartIndex = -1
                isInRange = False
            else:
                expression += self.to_regex_interpretable(chars[curIndex])
            curIndex += 1

        # Now we can append the unicode char classes if the user specified any.
        if len(self.unicodeClasses) > 0:
            for klass in self.unicodeClasses:
                expression += klass

        expression += MetaCharacters.CLOSE_SQUARE_BRACKET

        return expression

    def sto_regex(self):
        chars = sorted(list(self.codepoints))
        if not chars and not self.unicodeClasses:
            return ""
        expression = '['
        if self.negated:
            expression += '^'
        i = 0
        while i < len(chars):
            j = i
            while j + 1 < len(chars) and chars[j + 1] == chars[j] + 1:
                j += 1
            expression += self.to_regex_interpretable(chars[i])
            if j != i:
                expression += '-' + self.to_regex_interpretable(chars[j])
            i = j + 1

        for klass in self.unicodeClasses:
            expression += klass
        expression += ']'

        return expression

    @staticmethod
    def to_regex_interpretable(codepoint):
        if 0x00 <= codepoint <= 0x1F or 0x7F <= codepoint <= 0x9F:
            return "\\x{0:02X}".format(codepoint)
        if codepoint >= 0x10000:
            return "\\x{{{}}}".format(hex(codepoint)[2:])
        char_repr = chr(codepoint)
        if SET_RESTRICTED.match(char_repr):
            return "\\" + char_repr
        return char_repr
