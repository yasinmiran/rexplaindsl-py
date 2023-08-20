from unittest import TestCase

from rexplaindsl.complex.trie_expression import TrieExpression


class TestTrieExpression(TestCase):

    def test_should_minimize_string(self):
        trie = TrieExpression()
        trie.insert("Apple")
        trie.insert("Application")
        trie.insert("Appeal")
        self.assertEqual(trie.to_regex(), "App(?:eal|l(?:ication|e))")
