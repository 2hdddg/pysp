from pysp.ast import types


class BuiltInFunction(object):
    def __init__(self, environment, impl):
        self.environment = environment
        self.impl = impl
        self.type = types.CLOSURE

    def apply(self, values, frame):
        return self.impl(values)


def _plus(values):
    def get_number(p):
        return int(p.value)

    def acc(x, y):
        return x + y

    numbers = map(get_number, values)
    sum = reduce(acc, numbers)
    return types.Number(sum)

builtins = {
    '+': lambda e: BuiltInFunction(e, _plus),
}


def add_builtins_to_environment(environment):
    for symbol, func in builtins.iteritems():
        environment.bind(symbol, func(environment))
