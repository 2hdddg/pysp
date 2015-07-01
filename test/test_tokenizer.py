# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import *


def util_print_tokens(tokens):
    for t in tokens:
        print t


def util_get_tokens(code):
    tokenizer = Tokenizer(code)
    return list(tokenizer.get_tokens())


class TestTokenizer(unittest.TestCase):

    def test_can_tokenize_a_symbol(self):
        token = util_get_tokens('sym')[0]

        self.assertEqual(token['type'], 'symbol')

    def test_can_tokenize_a_number(self):
        token = util_get_tokens('1234')[0]

        self.assertEqual(token['type'], 'number')

    def test_can_tokenize_a_comment(self):
        token = util_get_tokens(';comment')[0]

        self.assertEqual(token['type'], 'comment')

    def test_can_tokenize_symbol_with_operators_without_white_space(self):
        tokens = util_get_tokens('(n1)')

        self.assertEqual(tokens[0]['type'], 'blockstart')
        self.assertEqual(tokens[1]['type'], 'symbol')
        self.assertEqual(tokens[2]['type'], 'blockend')
