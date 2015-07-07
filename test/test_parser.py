# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import Tokenizer
from pysp.parser import *


class TestParser(unittest.TestCase):

    def _print_tokens(self, tokens):
        """ When shit hits the fan
        """
        for t in tokens:
            print t

    def _get_ast(self, code):
        tokens = Tokenizer(code).next()
        parser = Parser(tokens)

        return parser.get_ast()

    def test_can_parse_a_number_into_a_number_atom(self):
        code = '''
        12
        '''
        ast = self._get_ast(code)

        number = ast.children[0]
        self.assertIsInstance(number, Atom)
        self.assertIsInstance(number, Number)
        self.assertEqual(number.value, 12)

    def test_can_parse_a_string_into_a_string_atom(self):
        code = '''
        "a string"
        '''
        ast = self._get_ast(code)

        number = ast.children[0]
        self.assertIsInstance(number, Atom)
        self.assertIsInstance(number, String)
        self.assertEqual(number.value, 'a string')

    def test_can_parse_a_symbol_into_a_symbol(self):
        code = '''
        the_symbol
        '''
        ast = self._get_ast(code)

        symbol = ast.children[0]
        self.assertIsInstance(symbol, Symbol)
        self.assertEqual(symbol.value, 'the_symbol')

    def test_can_parse_nesting_into_nodetree(self):
        code = '''
        (top (nested1)(nested2))
        '''
        ast = self._get_ast(code)

        top_node = ast.children[0]
        self.assertIsInstance(top_node, Node)
        self.assertIsInstance(top_node.children[0], Symbol)
        self.assertEqual(top_node.children[0].value, 'top')

        top_symbol = top_node.children[0]
        self.assertIsInstance(top_symbol, Symbol)
        self.assertEqual(top_symbol.value, 'top')

        nested1_node = top_node.children[1]
        self.assertIsInstance(nested1_node, Node)
        self.assertIsInstance(nested1_node.children[0], Symbol)
        self.assertEqual(nested1_node.children[0].value, 'nested1')

        nested2_node = top_node.children[2]
        self.assertIsInstance(nested2_node, Node)
        self.assertIsInstance(nested2_node.children[0], Symbol)
        self.assertEqual(nested2_node.children[0].value, 'nested2')

    def test_can_parse_constant_definition(self):
        code = '(define pi 3)'
        ast = self._get_ast(code)

        definition = ast.children[0]
        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.name, 'pi')
        self.assertIsInstance(definition.value, Number)

    def test_can_parse_lambda(self):
        code = '''
        (lambda (param1 param2) param2)
        '''
        ast = self._get_ast(code)

        closure = ast.children[0]

        self.assertIsInstance(closure, Closure)
        # Parameters
        self.assertEqual(len(closure.parameters), 2)
        self.assertEqual(closure.parameters[0], 'param1')
        self.assertEqual(closure.parameters[1], 'param2')
        # Body
        self.assertIsInstance(closure.body, Symbol)

    def test_can_parse_lambda_defintion(self):
        code = '''
        (define what (lambda (param1 param2) param2))
        '''
        ast = self._get_ast(code)

        definition = ast.children[0]
        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.name, 'what')
        closure = definition.value
        self.assertIsInstance(closure, Closure)
        # Parameters
        self.assertEqual(len(closure.parameters), 2)
        self.assertEqual(closure.parameters[0], 'param1')
        self.assertEqual(closure.parameters[1], 'param2')
        # Body
        self.assertIsInstance(closure.body, Symbol)

    def test_can_parse_definition_of_function_without_lambda(self):
        code = '''
        (define (what param1 param2) param2)
        '''

        ast = self._get_ast(code)

        definition = ast.children[0]
        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.name, 'what')
        closure = definition.value
        self.assertIsInstance(closure, Closure)
        # Parameters
        self.assertEqual(len(closure.parameters), 2)
        self.assertEqual(closure.parameters[0], 'param1')
        self.assertEqual(closure.parameters[1], 'param2')
        # Body
        self.assertIsInstance(closure.body, Symbol)
