import parser
from pexceptions import MissingSymbolError, NoFunctionError


class Scope(object):
    def __init__(self, parent):
        self.parent = parent
        self.definitions = {}

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

        def evaluate_atom(ast):
            runtime_class = _atoms[ast.__class__]
            return runtime_class(ast.value)

        def evaluate_node(ast):
            next = self.nest()
            return next.execute(ast)

        def evaluate_child(child):
            if isinstance(child, parser.Atom):
                return evaluate_atom(child)

            if isinstance(child, parser.Node):
                return evaluate_node(child)

            if isinstance(child, parser.Symbol):
                return evaluate_symbol(child)

            # Built-in function
            if isinstance(child, Function):
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
