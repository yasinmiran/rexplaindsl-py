class MetaCharacters:
    # Special Characters
    BACKSLASH = '\\'
    PAREN_OPEN = '('
    PAREN_CLOSE = ')'
    LESS_THAN = '<'
    GREATER_THAN = '>'
    OPEN_CURLY_BRACE = '{'
    CLOSE_CURLY_BRACE = '}'
    OPEN_SQUARE_BRACKET = '['
    CLOSE_SQUARE_BRACKET = ']'
    CARAT = '^'
    DOLLAR = '$'
    HYPHEN = '-'
    PLUS = '+'
    ASTERISK = '*'  # Kleene Star
    QUESTION_MARK = '?'
    COLON = ':'
    COMMA = ','
    PERIOD = '.'  # Matches Any

    # Anchor classes
    WORD_BOUNDARY = BACKSLASH + "b"
    NON_WORD_BOUNDARY = BACKSLASH + "B"
    BEGINNING_OF_TEXT = BACKSLASH + "A"
    END_OF_TEXT = BACKSLASH + "z"

    # Quotes
    QUOTE_START = BACKSLASH + "Q"
    QUOTE_END = BACKSLASH + "E"

    # Logical operators
    ALTERNATION = "|"

    # Concatenation is just appending two strings...
    # So, no special meta character for that.

    # Groups
    NAMED_CAPTURE_GROUP_PREFIX = "P"
