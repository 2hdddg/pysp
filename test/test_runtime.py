# -*- coding: utf-8 -*-
import unittest

from pysp.tokenizer import Tokenizer
from pysp.parser import Parser
from pysp.runtime import *


class TestRuntime(unittest.TestCase):


    def execute(self, code):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.get_tokens()
        parser = Parser(tokens)
        ast = parser.get_ast()
        scope = Scope()
        result = scope.execute(ast)
        return result

    def test_a_number_is_evaluated_as_a_number(self):
        code = '12'
        result = self.execute(code)

        self.assertEqual(result.value, 13)

