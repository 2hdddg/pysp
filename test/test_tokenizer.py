# -*- coding: utf-8 -*-
import unittest

from pysp.pexceptions import *
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

    def test_can_tokenize_a_string_with_apostrophes(self):
        token = util_get_tokens("'str'")[0]

        self.assertEqual(token['type'], 'string')
        self.assertEqual(token['value'], 'str')

    def test_can_tokenize_a_string_with_quotes(self):
        token = util_get_tokens('"str"')[0]

        self.assertEqual(token['type'], 'string')
        self.assertEqual(token['value'], 'str')

    def test_quoted_string_can_contain_apostrophes(self):
        token = util_get_tokens('''
                "'"
            ''')[0]

        self.assertEqual(token['type'], 'string')
        self.assertEqual(token['value'], "'")

    def test_apostrophed_string_can_contain_quotes(self):
        token = util_get_tokens('''
                '"'
            ''')[0]

        self.assertEqual(token['type'], 'string')
        self.assertEqual(token['value'], '"')

    def test_unfinished_string_raises_error(self):
        code = '''
            "started..but not ended
        '''

        def raises():
            util_get_tokens(code)

        self.assertRaises(UnexpectedEnd, raises)

    def test_can_tokenize_a_line_comment(self):
        token = util_get_tokens(';comment')[0]

        self.assertEqual(token['type'], 'comment')

    def test_can_tokenize_symbol_with_operators_without_white_space(self):
        tokens = util_get_tokens('(n1)')

        self.assertEqual(tokens[0]['type'], 'blockstart')
        self.assertEqual(tokens[1]['type'], 'symbol')
        self.assertEqual(tokens[2]['type'], 'blockend')

    def test_can_tokenize_line_comment_number_and_line_comment(self):
        tokens = util_get_tokens('''
            ; line 1
            1024
            ; line 2
            ''')

        self.assertEqual(tokens[0]['type'], 'comment')
        self.assertEqual(tokens[1]['type'], 'number')
        self.assertEqual(tokens[0]['type'], 'comment')

    def test_symbol_can_contain_question_mark(self):
        token = util_get_tokens('symb?')[0]

        self.assertEqual(token['type'], 'symbol')
        self.assertEqual(token['value'], 'symb?')
