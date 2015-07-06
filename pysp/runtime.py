import parser
from pexceptions import MissingSymbolError, NoFunctionError


class Scope(object):
    def __init__(self, parent):
        self.parent = parent
        self.definitions = {}

    def nest(self):
        return Scope(parent=self)

    def _apply_closure(self, closure, rest):
        for i, p in enumerate(closure.parameters):
            v = rest[i]
            self.definitions[p.value] = v
        return self.execute(closure.body)

    def _apply(self, evaluated):
        try:
            func = evaluated.pop(0)
        except IndexError:
            raise NoFunctionError("Empty...")

        if isinstance(func, BuiltInFunction):
            return func.apply(self, evaluated)
        if isinstance(func, parser.Closure):
            return self._apply_closure(func, evaluated)
        else:
            message = "Cannot execute %s as function" % func
            raise NoFunctionError(message)

    def find_symbol(self, name):
        if name in self.definitions:
            return self.definitions[name]

        if self.parent:
            return self.parent.find_symbol(name)

        return None

    def execute(self, node):
        def find_symbol(name):
            symbol = self.find_symbol(name)
            if not symbol:
                raise MissingSymbolError(name)
            return symbol

        def evaluate_symbol(ast):
            return evaluate_child(find_symbol(ast.value))

        def evaluate_node(ast):
            next = self.nest()
            return next.execute(ast)

        def evaluate_child(child):
            if isinstance(child, parser.Node):
                return evaluate_node(child)

            if isinstance(child, parser.Symbol):
                return evaluate_symbol(child)

            return child

        def evaluate(node):
            evaluated = []
            for child in node.children:
                result = evaluate_child(child)
                if result is not None:
                    evaluated.append(result)
            return evaluated

        def define(node):
            for child in node.children:
                if isinstance(child, parser.Definition):
                    self.definitions[child.name] = child.value

        define(node)
        evaluated = evaluate(node)
        return self._apply(evaluated)


class Global(Scope):
    def __init__(self):
        self.parent = None
        self.definitions = _symbols

    def _apply(self, evaluated):
        return evaluated.pop()


class BuiltInFunction(object):
    def __init__(self, apply):
        self.apply = apply


def builtin_plus(scope, parameters):
    def get_number(p):
        return int(p.value)

    def acc(x, y):
        return x + y

    numbers = map(get_number, parameters)
    sum = reduce(acc, numbers)
    return parser.Number(sum)


_symbols = {
    '+': BuiltInFunction(builtin_plus)
}
