# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import Tokenizer, token
from pysp.parser import Parser


class TestParser(unittest.TestCase):

    def _get_sexp(self, code):
        tokens = Tokenizer(code).next()
        parser = Parser(tokens)

        return parser.parse()

    def _get_raw(self, sexp):
        raw = []
        for x in sexp:
            if type(x) is token.Token:
                raw.append(x.value)
            else:
                raw.append(self._get_raw(x))
        return raw

    def test_can_parse_a_number(self):
        code = '''
        12
        '''
        parsed = self._get_sexp(code)

        self.assertEqual(self._get_raw(parsed), ['12'])

    def test_can_parse_nested_expression(self):
        code = '''
        (+ 5 (+ 3 5))
        '''
        parsed = self._get_sexp(code)

        '''
        [['+', '5', ['+', '3', '5']]
        '''

        self.assertEqual(self._get_raw(parsed), [['+', '5', ['+', '3', '5']]])
