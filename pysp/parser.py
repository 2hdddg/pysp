from pexceptions import ParserError

"""
    (define id expr)
        (define pi 3.14)
        (define salutation (list-ref '("Hi" "Hello") (random 2)))

    (define id (lambda (arg ...) body ...))

    (define (id arg ...) body ...)
        (define (greet name)
          (string-append salutation ", " name))

    (map '(1, 2, 3), (lambda (x)()))
"""


class Parser(object):
    def __init__(self, tokens):
        self._tokens = tokens

    def get_ast(self):

        def get_next_token():
            try:
                return self._tokens.next()
            except StopIteration:
                return None

        def parse_number(node, token):
            atom = Number(token)
            node.add_child(atom)

        def parse_string(node, token):
            atom = String(token)
            node.add_child(atom)

        def parse_symbol(node, token):
            atom = Symbol(token)
            node.add_child(atom)

        def parse_operator(node, token):
            atom = Symbol(token)
            node.add_child(atom)

        def parse_token(node, token):
            type = token['type']

            if type == 'number':
                return parse_number(node, token)
            if type == 'string':
                return parse_string(node, token)
            if type == 'symbol':
                return parse_symbol(node, token)
            if type == 'operator':
                return parse_operator(node, token)

        def build_lambda(tail):
            if len(tail) != 2:
                raise ParserError('Lambda needs 2')

            parameters_node = tail[0]
            parameters = parameters_node.children
            body = tail[1]

            closure = Closure(parameters, body)
            return closure

        def build_definition(tail):
            if len(tail) != 2:
                raise ParserError('Define needs 2')

            name = tail[0]
            if not isinstance(name, Symbol):
                raise ParserError('Define needs name')

            value = tail[1]

            return Definition(name.value, value)

        def analyze(node):
            if node.number_of_children == 0:
                return node

            children = node.children
            first = children[0]
            if isinstance(first, Symbol):
                value = first.value
                if value == 'lambda':
                    return build_lambda(children[1:])

                if value == 'define':
                    return build_definition(children[1:])

            return node

        def parse(node):
            while True:
                token = get_next_token()
                if not token:
                    raise ParserError("Expected token")

                type = token['type']

                if type == 'blockend':
                    break

                if type == 'blockstart':
                    node.add_child(parse(Node(parent=node)))
                else:
                    parse_token(node, token)
            return analyze(node)

        def parse_root():
            root = Root()
            while True:
                token = get_next_token()
                if not token:
                    break

                type = token['type']

                if type == 'blockend':
                    raise ParserError('Too many )?')

                if type == 'blockstart':
                    root.add_child(parse(Node(parent=root)))
                else:
                    parse_token(root, token)
            return root

        root = parse_root()

        hanging_token = get_next_token()
        if hanging_token:
            raise ParserError("hanging")

        return root


class Root(object):
    def __init__(self):
        self.children = []

    def get_parent(self):
        return None

    def add_child(self, child):
        self.children.append(child)

    def number_of_children(self):
        return len(self.children)

    def output(self, indent, out):
        out(indent * ' ' + str(self))
        indent += 1
        for child in self._children:
            child.output(indent, out)

    def __str__(self):
        return 'root'


class Node(Root):
    def __init__(self, parent=None):
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

    def output(self, indent, out):
        out(indent * ' ' + str(self))


class Number(Atom):
    def __str__(self):
        return 'number:%s' % self.value


class String(Atom):
    def __str__(self):
        return 'string:%s' % self.value


class Symbol(object):
    def __init__(self, token):
        self.value = token['value']

    def output(self, indent, out):
        out(indent * ' ' + str(self))

    def __str__(self):
        return 'symbol:%s' % self.value


class Definition(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Closure(object):
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body
