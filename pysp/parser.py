from pexceptions import ParserError

"""
    (define id expr)
        (define pi 3.14)
        (define salutation (list-ref '("Hi" "Hello") (random 2)))

    (define id (lambda (arg ...) body ...))

    (define (id arg ...) body ...)
        (define (greet name)
          (string-append salutation ", " name))
"""


class Parser(object):
    def __init__(self, tokens):
        self._tokens = tokens

    def get_ast(self):
        token_iterator = iter(self._tokens)

        def get_next_token():
            try:
                return token_iterator.next()
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

        def parse_other(node, token):
            type = token['type']

            if type == 'number':
                return parse_number(node, token)
            if type == 'string':
                return parse_string(node, token)
            if type == 'symbol':
                return parse_symbol(node, token)
            if type == 'operator':
                return parse_operator(node, token)

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
                    parse_other(node, token)
            return node

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
                    parse_other(root, token)
            return root

        root = parse_root()

        hanging_token = get_next_token()
        if hanging_token:
            raise ParserError("hanging")

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

    def number_of_children(self):
        return len(self._children)

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
