# -*- coding: utf-8 -*-
import unittest

from pysp.errors import *
from pysp.tokenizer import token, Tokenizer


def util_print_tokens(tokens):
    for t in tokens:
        print t


def util_get_tokens(code):
    return Tokenizer(code).next()


class TestTokenizer(unittest.TestCase):

    def test_can_tokenize_a_symbol(self):
        tokens = util_get_tokens('sym')
        t = tokens.next()

        self.assertEqual(t.type, token.SYMBOL)

    def test_can_tokenize_a_number(self):
        tokens = util_get_tokens('1234')
        t = tokens.next()

        self.assertEqual(t.type, token.NUMBER)

    def test_can_tokenize_a_string_with_apostrophes(self):
        t = util_get_tokens("'str'").next()

        self.assertEqual(t.type, token.STRING)
        self.assertEqual(t.value, 'str')

    def test_can_tokenize_a_string_with_quotes(self):
        t = util_get_tokens('"str"').next()

        self.assertEqual(t.type, token.STRING)
        self.assertEqual(t.value, 'str')

    def test_quoted_string_can_contain_apostrophes(self):
        t = util_get_tokens('''
                "'"
            ''').next()

        self.assertEqual(t.type, token.STRING)
        self.assertEqual(t.value, "'")

    def test_apostrophed_string_can_contain_quotes(self):
        t = util_get_tokens('''
                '"'
            ''').next()

        self.assertEqual(t.type, token.STRING)
        self.assertEqual(t.value, '"')

    def test_unfinished_string_raises_error(self):
        code = '''
            "started..but not ended
        '''

        def raises():
            util_get_tokens(code).next()

        self.assertRaises(UnexpectedEnd, raises)

    def test_can_tokenize_a_line_comment(self):
        t = util_get_tokens(';comment').next()

        self.assertEqual(t.type, token.COMMENT)

    def test_can_tokenize_symbol_with_operators_without_white_space(self):
        tokens = util_get_tokens('(n1)')

        self.assertEqual(tokens.next().type, token.BLOCKSTART)
        self.assertEqual(tokens.next().type, token.SYMBOL)
        self.assertEqual(tokens.next().type, token.BLOCKEND)

    def test_can_tokenize_line_comment_number_and_line_comment(self):
        tokens = util_get_tokens('''
            ; line 1
            1024
            ; line 2
            ''')

        self.assertEqual(tokens.next().type, token.COMMENT)
        self.assertEqual(tokens.next().type, token.NUMBER)
        self.assertEqual(tokens.next().type, token.COMMENT)

    def test_symbol_can_contain_question_mark(self):
        t = util_get_tokens('symb?').next()

        self.assertEqual(t.type, token.SYMBOL)
        self.assertEqual(t.value, 'symb?')
