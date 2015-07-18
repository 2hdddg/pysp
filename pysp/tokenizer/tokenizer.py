from pysp.errors import UnexpectedEnd
import token

Token = token.Token


def _process(c, state, row, column):
    tokens = []

    if state:
        tokens, c, state = state(c, row, column)

        if not c:
            return tokens, None, state

    if c.isspace():
        pass

    elif c in ('+', '-', '*', '/'):
        tokens.append(Token(token.OPERATOR, c, row, column))

    elif c == '(':
        tokens.append(Token(token.BLOCKSTART, c, row, column))

    elif c == ')':
        tokens.append(Token(token.BLOCKEND, c, row, column))

    elif c in ('"', "'"):

        string = Token(token.STRING, '', row, column)

        def next_string(next_c, next_row, next_column):
            if c == next_c:
                return [string], None, None
            string.value += next_c
            return [], None, next_string

        state = next_string

    elif c.isdigit():

        number = Token(token.NUMBER, c, row, column)

        def next_number(next_c, next_row, next_column):
            if next_c.isdigit():
                number.value += next_c
                return [], None, next_number
            if next_c == '.':
                number.value += next_c
                return [], None, next_number
            else:
                return [number], next_c, None

        state = next_number

    elif c == ';':
        comment = Token(token.COMMENT, c, row, column)

        def next_comment(next_c, next_row, next_column):
            if next_row > row:
                return [comment], next_c, None

            comment.value += next_c
            return [], None, next_comment

        state = next_comment

    elif c.isalpha():

        symbol = Token(token.SYMBOL, c, row, column)

        def next_symbol(next_c, next_row, next_column):
            if next_c.isalpha() or next_c.isdigit() or next_c in ('?', '_'):
                symbol.value += next_c
                return [], None, next_symbol
            else:
                return [symbol], next_c, None

        state = next_symbol

    return tokens, None, state


class Tokenizer(object):
    def __init__(self,  input):
        self._input = input

    def _get_lines(self):
        return self._input.splitlines(True)

    def __iter__(self):
        return self.next()

    def next(self):
        state = None
        for row, line in enumerate(self._get_lines()):
            for column, char in enumerate(line):
                tokens, char, state = _process(char, state, row, column)
                for t in tokens:
                    yield t

        # Flush
        row += 1
        tokens, char, state = _process(' ', state, row, 0)
        for t in tokens:
            yield t

        if state:
            raise UnexpectedEnd('Still in state: ' + str(state))
