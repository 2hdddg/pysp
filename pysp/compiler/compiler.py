from pysp.errors import ParserError
from pysp.tokenizer import token
import ast


class Compiler(object):
    def __init__(self, tokens):
        self._tokens = tokens
        self._keyword_parsers = {
            'lambda': self._parse_lambda,
            'define': self._parse_define,
        }
        self._type_converters = {
            'symbol': self._convert_symbol,
            'number': self._convert_number,
            'string': self._convert_string,
            'operator': self._convert_operator,
        }
        self.root = None

    def _next_token(self):
        try:
            return self._tokens.next()
        except StopIteration:
            return None

    def _raise(self, message):
        if self.root:
            self.root.show()
        else:
            print "Not even a root"
        raise ParserError(message)

    def _convert_symbol(self, t):
        return ast.Node(ast.SYMBOL, value=t.value)

    def _convert_operator(self, t):
        return ast.Node(ast.SYMBOL, value=t.value)

    def _convert_number(self, t):
        return ast.Node(ast.NUMBER, value=int(t.value))

    def _convert_string(self, t):
        return ast.Node(ast.STRING, value=t.value)

    def _add_parameters(self, node, first_is_value=False):
        """ Assumes position is after first '(',
        reads tokens and verifies them until
        end of tokens or ')'
        Adds valid tokens to specified node and
        raises on invalid
        """
        t = self._next_token()
        if not t.type == token.BLOCKSTART:
            self._raise("Expected (")

        t = self._next_token()
        found_value = False
        while not t.type == token.BLOCKEND:
            if not t:
                self._raise("Expected more")
            if not t.type == token.SYMBOL:
                self._raise("Expected symbol")

            if first_is_value and not found_value:
                node.value = t.value
                found_value = True
            else:
                node.add(ast.Node(ast.PARAMETER, value=t.value))

            t = self._next_token()

        if first_is_value and not found_value:
            self._raise("Expected name")

    def _parse_body(self, node):
        body = ast.Node(ast.BODY)
        t = self._next_token()

        while t:
            if t.type == token.BLOCKEND:
                break

            if t.type == token.BLOCKSTART:
                body.add(self._begin())
            else:
                body.add(self._convert(t))

            t = self._next_token()

        return body

    def _parse_lambda(self):
        node = ast.Node(ast.LAMBDA)

        self._add_parameters(node, first_is_value=False)
        node.add(self._parse_body(node))

        return node

    def _parse_define(self):
        definition = ast.Node(ast.DEFINITION)
        t = self._next_token()
        if t.type == token.SYMBOL:
            definition.value = t.value
            self._children(self._next_token(), definition)
            return definition
        else:
            self._raise('Illegal definition, needs name!')

    def _convert(self, t):
        converter = self._type_converters.get(t.type)
        if not converter:
            self._raise("Do not know what to do 1")

        converted = converter(t)
        return converted

    def _is_atom(self, type):
        return type in (token.NUMBER, token.STRING)

    def _begin(self):
        t = self._next_token()

        if t.type == token.SYMBOL:
            value = t.value

            parser = self._keyword_parsers.get(value)
            if parser:
                return parser()

        if t.type in (token.SYMBOL, token.OPERATOR, token.BLOCKSTART):
            application = ast.Node(ast.APPLICATION)
            self._children(t, application)

            return application

        if self._is_atom(t.type):
            self._raise("Cannot evaluate atom as function")

        self._raise("Do not know what to do 2")

    def _children(self, t, node):
        while t:
            if t.type == token.BLOCKEND:
                break
            elif t.type == token.BLOCKSTART:
                node.add(self._begin())
            else:
                node.add(self._convert(t))

            t = self._next_token()

    def compile(self):
        self.root = ast.Node(ast.ROOT)
        t = self._next_token()

        while t:

            if t.type == token.BLOCKEND:
                self._raise('Too many )?')
            elif t.type == token.BLOCKSTART:
                self.root.add(self._begin())
            else:
                self.root.add(self._convert(t))
            t = self._next_token()

        return self.root
