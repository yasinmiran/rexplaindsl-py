import re2

from rexplaindsl.exceptions import InvalidGroupNameException

VALID_GROUP_NAME = re2.compile(r"^[^[:punct:][:digit:][:space:]]\w{1,15}$")
RESERVED = re2.compile("[<(\\[{\\^\\-=$!|\\]})?*+.>/]")


def as_regex_literal(some_string) -> str:
    if len(some_string) == 1:
        return RESERVED.sub(r"\\\g<0>", some_string)
    composed = []
    i = 0
    while i < len(some_string):
        codepoint = ord(some_string[i])
        if len(some_string[i:]) > 1 and codepoint > 0xFFFF:  # Supplementary codepoint
            composed.append(f"\\x{{{hex(codepoint)[2:]}}}")
            i += 2  # Skip the surrogate pair
        else:  # BMP codepoint
            val = some_string[i]
            composed.append("\\" + val if RESERVED.match(val) else val)
            i += 1
    return "".join(composed)


def as_regex_group_name(name) -> str:
    if not VALID_GROUP_NAME.match(name):
        raise InvalidGroupNameException()
    return name


def to_codepoint(character) -> int:
    return ord(character[0]) if character else 0
