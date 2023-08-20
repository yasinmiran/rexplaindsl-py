from typing import Set

from rexplaindsl.api.expression import Expression
from rexplaindsl.api.meta_characters import MetaCharacters
from rexplaindsl.complex.trie_expression import TrieExpression
from rexplaindsl.dsl.groups import non_capture_group


def either(*expressions: Expression) -> Expression:
    alternations = MetaCharacters.ALTERNATION.join([expr.to_regex() for expr in expressions if expr])
    print(alternations)
    return non_capture_group(Expression(lambda: alternations))


def either_str(*strings: str) -> Expression:
    return either_strings_set(set(strings))


def either_strings_set(strings: Set[str]) -> Expression:
    trie = TrieExpression()
    trie.insert_all(strings)
    return trie


def concat(a: Expression, b: Expression) -> Expression:
    return Expression(lambda: a.to_regex() + b.to_regex())


def concat_multiple(*expressions: Expression) -> Expression:
    return Expression(lambda: "".join([expr.to_regex() for expr in expressions if expr]))
