# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import Tokenizer
from pysp.parser import Parser
from pysp.compiler import Compiler
from pysp.ast import ast


class TestCompiler(unittest.TestCase):

    def _print_tokens(self, tokens):
        """ When shit hits the fan
        """
        for t in tokens:
            print t

    def _get_ast(self, code):
        tokens = Tokenizer(code).next()
        parsed = Parser(tokens).parse()
        compiler = Compiler(parsed)

        return compiler.compile()

    def test_can_parse_a_number_into_a_number_atom(self):
        code = '''
        12
        '''
        parsed = self._get_ast(code)

        number = parsed.children[0]
        self.assertEqual(number.type, ast.NUMBER)
        self.assertEqual(number.value, 12)

    def test_can_parse_a_string_into_a_string_atom(self):
        code = '''
        "a string"
        '''
        parsed = self._get_ast(code)

        string = parsed.children[0]
        self.assertEqual(string.type, ast.STRING)
        self.assertEqual(string.value, 'a string')

    def test_can_parse_a_symbol_into_a_symbol(self):
        code = '''
        the_symbol
        '''
        parsed = self._get_ast(code)

        symbol = parsed.children[0]
        self.assertEqual(symbol.type, ast.SYMBOL)
        self.assertEqual(symbol.value, 'the_symbol')

    def test_can_parse_nesting_into_applications(self):
        code = '''
        (top (nested1)(nested2))
        '''
        parsed = self._get_ast(code)

        top = parsed.children[0]
        self.assertEqual(top.type, ast.APPLICATION)
        fun_name = top.children[0]
        self.assertEqual(fun_name.value, 'top')

        nested1 = top.children[1]
        self.assertEqual(nested1.type, ast.APPLICATION)
        fun_name = nested1.children[0]
        self.assertEqual(fun_name.value, 'nested1')

        nested2 = top.children[2]
        self.assertEqual(nested2.type, ast.APPLICATION)
        fun_name = nested2.children[0]
        self.assertEqual(fun_name.value, 'nested2')

    def test_can_parse_lambda(self):
        code = '''
        (lambda (param1 param2) thebody)
        '''
        parsed = self._get_ast(code)

        l = parsed.children[0]

        self.assertEqual(l.type, ast.LAMBDA)
        self.assertEqual(l.children[0].type, ast.PARAMETER)
        self.assertEqual(l.children[0].value, 'param1')
        self.assertEqual(l.children[1].type, ast.PARAMETER)
        self.assertEqual(l.children[1].value, 'param2')
        body = l.children[2]
        self.assertEqual(body.type, ast.BODY)
        self.assertEqual(body.children[0].type, ast.SYMBOL)
        self.assertEqual(body.children[0].value, 'thebody')

    def test_can_parse_constant_definition(self):
        code = '(define pi 3)'
        parsed = self._get_ast(code)

        definition = parsed.children[0]
        self.assertEqual(definition.type, ast.DEFINITION)
        self.assertEqual(definition.value, 'pi')
        number = definition.children[0]
        self.assertEqual(number.value, 3)
        self.assertEqual(len(definition.children), 1)

    def test_can_parse_lambda_defintion(self):
        code = '''
        (define what (lambda (param1 param2) the_body))
        '''
        parsed = self._get_ast(code)

        definition = parsed.children[0]
        self.assertEqual(definition.type, ast.DEFINITION)
        self.assertEqual(definition.value, 'what')
        the_lambda = definition.children[0]
        self.assertEqual(the_lambda.type, ast.LAMBDA)
        self.assertEqual(len(definition.children), 1)
        # Parameters
        self.assertEqual(the_lambda.children[0].type, ast.PARAMETER)
        self.assertEqual(the_lambda.children[1].type, ast.PARAMETER)
        # Body
        body = the_lambda.children[2]
        self.assertEqual(body.type, ast.BODY)
        self.assertEqual(len(body.children), 1)
        self.assertEqual(body.children[0].type, ast.SYMBOL)
        self.assertEqual(body.children[0].value, 'the_body')

"""

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
"""