# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import Tokenizer
from pysp.parser import Parser
from pysp.errors import *
from pysp.runtime import *


class TestRuntime(unittest.TestCase):

    def execute(self, code):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.next()
        parser = Parser(tokens)
        ast = parser.get_ast()
        g = Global()
        result = g.execute(ast)
        return result

    # Behaviour without any scope

    def test_a_number_results_in_number(self):
        code = '12'
        result = self.execute(code)

        self.assertEqual(result.value, 12)

    def test_a_string_results_in_a_string(self):
        code = "'str'"
        result = self.execute(code)

        self.assertEqual(result.value, 'str')

    def test_a_serie_of_atoms_results_in_last_atom(self):
        code = "1 'string' 3"
        result = self.execute(code)

        self.assertEqual(result.value, 3)

    # Defines
    def test_can_evaluate_a_defined_symbol(self):
        code = '''
            (define pi 3)

            pi
        '''
        result = self.execute(code)

        self.assertEqual(result.value, 3)

    def test_can_evaluate_a_defined_lambda(self):
        code = '''
            (define add (lambda (x y) (+ x y)))

            (add 3 4)
        '''
        result = self.execute(code)

        self.assertEqual(result.value, 7)

    def test_can_evaluate_a_defined_function(self):
        code = '''
            (define (add x y) (+ x y))

            (add 3 4)
        '''
        result = self.execute(code)

        self.assertEqual(result.value, 7)

    # Error handling

    def test_number_cannot_be_executed_as_function(self):
        def test():
            code = '(1)'
            self.execute(code)

        self.assertRaises(NoFunctionError, test)

    def test_call_to_function_with_too_few_params_should_raise(self):
        def test():
            code = '''
                (define add (lambda (x y) (+ x y)))

                (add 3)
            '''
            self.execute(code)

        self.assertRaises(ParameterError, test)

    # Built in functions

    # Add
    def test_can_add_two_ints(self):
        code = '(+ 1 2)'
        result = self.execute(code)

        self.assertEqual(result.value, 3)

    def test_can_add_series_of_ints(self):
        code = '(+ 1 2 3 4 5)'
        result = self.execute(code)

        self.assertEqual(result.value, 15)
