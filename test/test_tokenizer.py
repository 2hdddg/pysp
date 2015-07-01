# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import *


class TestTokenizer(unittest.TestCase):
    def _print_tokens(self, tokens):
        for t in tokens:
            print t

    def _get_tokens(self, code):
        tokenizer = Tokenizer(code)
        return list(tokenizer.get_tokens())

    def test_can_tokenize_a_symbol(self):
        tokens = self._get_tokens('sym')

        token = tokens[0]
        self.assertEqual(token['type'], 'symbol')

    def test_can_tokenize_symbol_with_operators_without_white_space(self):
        tokens = self._get_tokens('(n1)')

        self.assertEqual(tokens[0]['type'], 'blockstart')
        self.assertEqual(tokens[1]['type'], 'symbol')
        self.assertEqual(tokens[2]['type'], 'blockend')
