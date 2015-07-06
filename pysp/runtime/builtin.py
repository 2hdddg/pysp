import pysp.parser as parser


class BuiltInFunction(object):
    def __init__(self, apply):
        self.apply = apply


def _builtin_plus(scope, parameters):
    def get_number(p):
        return int(p.value)

    def acc(x, y):
        return x + y

    numbers = map(get_number, parameters)
    sum = reduce(acc, numbers)
    return parser.Number(sum)


symbols = {
    '+': BuiltInFunction(_builtin_plus)
}
