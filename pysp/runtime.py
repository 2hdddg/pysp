import parser
from pexceptions import MissingSymbolError, NoFunctionError


class Scope(object):
    def __init__(self, parent):
        self.parent = parent

    def nest(self):
        return Scope(parent=self)

    def _apply(self, evaluated):
        try:
            func = evaluated.pop(0)
        except IndexError:
            raise NoFunctionError("Empty...")

        if isinstance(func, Function):
            return func.apply(self, evaluated)
        else:
            raise NoFunctionError('Cannot execute xxx as function')

    def execute(self, node):
        def find_symbol(name):
            symbol = _symbols.get(name, None)
            if not symbol:
                raise MissingSymbolError(name)
            return symbol

        def evaluate_symbol(ast):
            return find_symbol(ast.value)

        def evaluate_atom(ast):
            runtime_class = _atoms[ast.__class__]
            return runtime_class(ast.value)

        def evaluate_node(ast):
            next = self.nest()
            return next.execute(ast)

        def evaluate(node):
            evaluated = []
            for child in node.children:
                if isinstance(child, parser.Atom):
                    evaluated.append(
                        evaluate_atom(child))

                if isinstance(child, parser.Node):
                    evaluated.append(
                        evaluate_node(child))

                if isinstance(child, parser.Symbol):
                    evaluated.append(
                        evaluate_symbol(child))
            return evaluated

        evaluated = evaluate(node)
        return self._apply(evaluated)


class Module(Scope):
    def __init__(self):
        self.parent = None

    def _apply(self, evaluated):
        return evaluated.pop()


class Type(object):
    def __init__(self, name):
        self.typename = name


class Number(object):
    def __init__(self, value):
        self.value = int(value)
        self.type = Type('number')

    def __str__(self):
        return repr(self.value)


class String(object):
    def __init__(self, value):
        self.value = str(value)
        self.type = Type('string')

    def __str__(self):
        return repr(self.value)


class Function(object):
    pass


class PlusFunction(Function):
    def apply(self, scope, parameters):
        def get_number(p):
            return int(p.value)

        def acc(x, y):
            return x + y

        numbers = map(get_number, parameters)
        sum = reduce(acc, numbers)
        return Number(sum)

_symbols = {
    '+': PlusFunction()
}

_atoms = {
    parser.Number: Number,
    parser.String: String,
}
