import pysp.ast as ast
from pysp.errors import ParameterError

CLOSURE = 'closure'


class Number(object):
    def __init__(self, value):
        self.value = int(value)
        self.type = ast.NUMBER

    def __str__(self):
        return 'number:%s' % self.value


class String(object):
    def __init__(self, value):
        self.value = value
        self.type = ast.STRING

    def __str__(self):
        return 'string:%s' % self.value


class Symbol(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'symbol:%s' % self.value


class Definition(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = ast.DEFINITION


class Closure(object):
    def __init__(self, parameters, body, environment):
        self.parameters = parameters
        self.body = body
        self.environment = environment
        self.type = CLOSURE

    def apply(self, values, frame):
        execution_environment = self.environment.nest()
        for index, parameter in enumerate(self.parameters):
            try:
                value = values[index]
            except IndexError:
                raise ParameterError("Too few parameters")

            execution_environment.bind(parameter, value)

        return frame.evaluate(self.body, execution_environment)
