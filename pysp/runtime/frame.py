import pysp.ast as ast

from .types import *
from .environment import Environment
from .builtin import add_builtins_to_environment


class Frame(object):
    def __init__(self, parent=None):
        self.parent = parent
        self._handlers = {
            ast.ROOT: self.evaluate_root,
            ast.BODY: self.evaluate_root,
            ast.NUMBER: self.evaluate_number,
            ast.STRING: self.evaluate_string,
            ast.SYMBOL: self.evaluate_symbol,
            ast.DEFINITION: self.evaluate_definition,
            ast.APPLICATION: self.evaluate_application,
            ast.LAMBDA: self.evaluate_lambda,
            CLOSURE: self.evaluate_closure,
        }

    def nest(self):
        return Frame(parent=self)

    def evaluate_root(self, ast, environment):
        result = None
        for child in ast.children:
            handler = self._handlers.get(child.type)
            if not handler:
                raise "Hell"
            result = handler(child, environment)
        return result

    def evaluate_definition(self, definition, environment):
        value = definition.children[0]
        environment.bind(definition.value, value)

    def evaluate_application(self, application, environment):
        evaluated = []
        for child in application.children:
            result = self.evaluate(child, environment)
            evaluated.append(result)

        function = evaluated[0]
        if not hasattr(function, 'apply'):
            raise "No function to apply"

        nested = self.nest()

        return function.apply(evaluated[1:], nested)

    def evaluate_lambda(self, l, environment):
        l.show()
        parameters = []
        for x in l.children:
            if x.type == ast.PARAMETER:
                parameters.append(x.value)

            if x.type == ast.BODY:
                return Closure(parameters, x, environment)

        raise "no body"

    def evaluate_closure(self, closure, environment):
        return closure

    def evaluate_number(self, number, environment):
        return Number(number.value)

    def evaluate_string(self, string, environment):
        return String(string.value)

    def evaluate_symbol(self, symbol, environment):
        value = environment.get_binding(symbol.value)
        return self.evaluate(value, environment)

    def evaluate(self, something, environment):
        handler = self._handlers.get(something.type)
        if not handler:
            raise "Hell"

        result = handler(something, environment)
        return result

    def execute(self, program):
        environment = Environment()
        add_builtins_to_environment(environment)

        result = self.evaluate(program, environment)
        return result
