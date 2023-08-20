from sortedcontainers import SortedDict

from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.utils.common import as_regex_literal

NULL_KEY = ""


class Node(Expression):

    def __init__(self):
        super().__init__(self.to_regex)
        self.nodes = SortedDict()
        self.alternations = []
        self.char_classes = []
        self.has_optionals = False
        self.has_character_classes = False

    def contains_key(self, char):
        return self.nodes.__contains__(char)

    def put(self, char, node):
        self.nodes.__setitem__(char, node)

    def get(self, char):
        return self.nodes.get(char)

    def synthesize_string_alternations(self):
        for key, value in self.nodes.items():
            escaped = as_regex_literal(key)
            if value is not None:
                sub_expression = value.to_regex()
                if sub_expression is not None:
                    self.alternations.append(escaped + sub_expression)
                else:
                    self.char_classes.append(escaped)
            else:
                self.has_optionals = True

    def synthesize_character_classes(self):
        self.has_character_classes = not self.alternations
        if self.char_classes:
            if len(self.char_classes) == 1:
                self.alternations.append(self.char_classes[0])
            else:
                set_chars = MetaCharacters.OPEN_SQUARE_BRACKET + "".join(
                    self.char_classes) + MetaCharacters.CLOSE_SQUARE_BRACKET
                self.alternations.append(set_chars)

    def to_regex(self):
        if NULL_KEY in self.nodes and len(self.nodes) == 1:
            return None

        self.synthesize_string_alternations()
        self.synthesize_character_classes()

        expression = []

        if len(self.alternations) == 1:
            expression.append(self.alternations[0])
        else:
            expression.append(MetaCharacters.PAREN_OPEN + MetaCharacters.QUESTION_MARK + MetaCharacters.COLON)
            expression.append(MetaCharacters.ALTERNATION.join(self.alternations))
            expression.append(MetaCharacters.PAREN_CLOSE)

        if self.has_optionals:
            if self.has_character_classes:
                return "".join(expression) + MetaCharacters.QUESTION_MARK
            else:
                return MetaCharacters.PAREN_OPEN + MetaCharacters.QUESTION_MARK + MetaCharacters.COLON + "".join(
                    expression) + MetaCharacters.PAREN_CLOSE + MetaCharacters.QUESTION_MARK

        return "".join(expression)


class TrieExpression(Expression):

    def __init__(self):
        super().__init__(self.to_regex)
        self.root = Node()

    def insert(self, word):
        current = self.root
        for c in word:
            if not current.contains_key(c):
                current.put(c, Node())
            current = current.get(c)
        current.put(NULL_KEY, None)

    def insert_all(self, words):
        for word in words:
            self.insert(word)

    def to_regex(self):
        return self.root.to_regex()
