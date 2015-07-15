from errors import ParserError
import ast


class Parser(object):
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

    def _convert_symbol(self, token):
        return ast.Node(ast.SYMBOL, value=token['value'])

    def _convert_operator(self, token):
        return ast.Node(ast.SYMBOL, value=token['value'])

    def _convert_number(self, token):
        value = int(token['value'])
        return ast.Node(ast.NUMBER, value=value)

    def _convert_string(self, token):
        value = token['value']
        return ast.Node(ast.STRING, value=value)

    def _add_parameters(self, node, first_is_value=False):
        """ Assumes position is after first '(',
        reads tokens and verifies them until
        end of tokens or ')'
        Adds valid tokens to specified node and
        raises on invalid
        """
        token = self._next_token()
        if not token['type'] == 'blockstart':
            self._raise("Expected (")

        token = self._next_token()
        found_value = False
        while not token['type'] == 'blockend':
            if not token:
                self._raise("Expected more")
            if not token['type'] == 'symbol':
                self._raise("Expected symbol")

            if first_is_value and not found_value:
                node.value = token['value']
                found_value = True
            else:
                node.add(ast.Node(ast.PARAMETER, value=token['value']))

            token = self._next_token()

        if first_is_value and not found_value:
            self._raise("Expected name")

    def _parse_body(self, node):
        body = ast.Node(ast.BODY)
        token = self._next_token()

        while token:
            if token['type'] == 'blockend':
                break

            if token['type'] == 'blockstart':
                body.add(self._begin())
            else:
                body.add(self._convert(token))

            token = self._next_token()

        return body

    def _parse_lambda(self):
        node = ast.Node(ast.LAMBDA)

        self._add_parameters(node, first_is_value=False)
        node.add(self._parse_body(node))

        return node

    def _parse_define(self):
        definition = ast.Node(ast.DEFINITION)
        name = self._next_token()
        if name['type'] == 'symbol':
            definition.value = name['value']
            self._children(self._next_token(), definition)
            return definition
        else:
            self._raise('Illegal definition, needs name!')

    def _convert(self, token):
        converter = self._type_converters.get(token['type'])
        if not converter:
            self._raise("Do not know what to do 1")

        converted = converter(token)
        return converted

    def _is_atom(self, type):
        return type in ('number', 'string')

    def _begin(self):
        token = self._next_token()

        if token['type'] == 'symbol':
            value = token['value']

            parser = self._keyword_parsers.get(value)
            if parser:
                return parser()

        if token['type'] in ('symbol', 'operator', 'blockstart'):
            application = ast.Node(ast.APPLICATION)
            self._children(token, application)

            return application

        if self._is_atom(token['type']):
            self._raise("Cannot evaluate atom as function")

        self._raise("Do not know what to do 2")

    def _children(self, token, node):
        while token:
            if token['type'] == 'blockend':
                break
            elif token['type'] == 'blockstart':
                node.add(self._begin())
            else:
                node.add(self._convert(token))

            token = self._next_token()

    def parse(self):
        self.root = ast.Node(ast.ROOT)
        token = self._next_token()

        while token:

            if token['type'] == 'blockend':
                self._raise('Too many )?')
            elif token['type'] == 'blockstart':
                self.root.add(self._begin())
            else:
                self.root.add(self._convert(token))
            token = self._next_token()

        return self.root
