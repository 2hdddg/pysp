from pexceptions import ParserError
import runtime


class Parser(object):
    def __init__(self, tokens):
        self._tokens = tokens

    def get_ast(self):
        def parse(node, token):
            type = token['type']
            leaf = leafs.get(type, None)
            if leaf:
                child = leaf(token)
                node.add_child(child)
                return node

            if type == 'blockstart':
                child = Node(parent=node)
                node.add_child(child)
                return child

            if type == 'blockend':
                parent = node.get_parent()
                if not parent:
                    message = "Misplaced blockend in token:" + str(token)
                    raise ParserError(message)
                return parent

        root = Root()
        node = root

        for token in self._tokens:
            node = parse(node, token)

        if node != root:
            raise ParserError("Missing blockend")

        return root


class Root(object):
    def __init__(self):
        self._children = []

    def get_parent(self):
        return None

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children

    def output(self, indent, out):
        out(indent * ' ' + str(self))
        indent += 1
        for child in self._children:
            child.output(indent, out)

    def __str__(self):
        return 'root'


class Node(Root):
    def __init__(self, parent):
        super(Node, self).__init__()
        self._parent = parent
        self._is_open = True

    def get_parent(self):
        return self._parent

    def __str__(self):
        return 'node'


class Atom(object):
    def __init__(self, token):
        self.value = token['value']

    def get_runtime_instance(self):
        raise "missing"

    def output(self, indent, out):
        out(indent * ' ' + str(self))


class NumberAtom(Atom):
    def get_runtime_instance(self):
        return runtime.Number(self.value)

    def __str__(self):
        return 'number:%s' % self.value


class StringAtom(Atom):
    def __str__(self):
        return 'string:%s' % self.value


class Symbol(object):
    def __init__(self, token):
        self.value = token['value']

    def output(self, indent, out):
        out(indent * ' ' + str(self))

    def __str__(self):
        return 'symbol:%s' % self.value


leafs = {
    'number': NumberAtom,
    'string': StringAtom,
    'symbol': Symbol,
    'operator': Symbol
}


if __name__ == "__main__":
    from tokenizer import Tokenizer

    def print_ast(code):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)
        ast = parser.get_ast()

        def out(s):
            print s

        print "Code:"
        print code
        print "Output:"
        ast.output(indent=2, out=out)

    code = '''
        12
    '''
    print_ast(code)

    code = '''
        (abc 1 2 'str')
    '''
    print_ast(code)

    code = '''
        (+ (* 2 2) (/ 6 3))
    '''
    print_ast(code)
