from pysp.errors import UnexpectedEnd
import token

Token = token.Token

_block_start = ('(')
_block_end = (')')
_operator = ('+', '-', '*', '/')
_string_start = ('"', "'")
_comment_start = (';')
_whitespace = (' ', '\t', '\n')
_digit = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
_decimal = ('.')
_allowed_in_symbol = ('?', '_')


def _is(l, c):
    return c in l


def _is_alpha(c):
    return c.isalpha()


def _blockstart_token(block, row, column):
    return Token(token.BLOCKSTART, block, row, column)


def _blockend_token(block, row, column):
    return Token(token.BLOCKEND, block, row, column)


def _string_token(contents, row, column):
    return Token(token.STRING, contents, row, column)


def _number_token(number, row, column):
    return Token(token.NUMBER, number, row, column)


def _operator_token(operator, row, column):
    return Token(token.OPERATOR, operator, row, column)


def _symbol_token(symbol, row, column):
    return Token(token.SYMBOL, symbol, row, column)


def _comment_token(comment, row, column):
    return Token(token.COMMENT, comment, row, column)


class Tokenizer(object):
    def __init__(self,  input):
        self._input = input

    def _get_lines(self):
        return self._input.splitlines(True)

    def __iter__(self):
        return self.next()

    def next(self):

        def process(c, state, row, column):
            tokens = []

            if state:
                tokens, c, state = state(c, row, column)

                if not c:
                    return tokens, None, state

            if _is(_whitespace, c):
                pass

            elif _is(_operator, c):
                tokens.append(_operator_token(c, row, column))

            elif _is(_block_start, c):
                tokens.append(_blockstart_token(c, row, column))

            elif _is(_block_end, c):
                tokens.append(_blockend_token(c, row, column))

            elif _is(_string_start, c):

                string = _string_token('', row, column)

                def next_string(next_c, next_row, next_column):
                    if c == next_c:
                        return [string], None, None
                    string.value += next_c
                    return [], None, next_string

                state = next_string

            elif _is(_digit, c):

                number = _number_token(c, row, column)

                def next_number(next_c, next_row, next_column):
                    if _is(_digit, next_c):
                        number.value += next_c
                        return [], None, next_number
                    if _is(_decimal, next_c):
                        number.value += next_c
                        return [], None, next_number
                    else:
                        return [number], next_c, None

                state = next_number

            elif _is(_comment_start, c):
                comment = _comment_token(c, row, column)

                def next_comment(next_c, next_row, next_column):
                    if next_row > row:
                        return [comment], next_c, None

                    comment.value += next_c
                    return [], None, next_comment

                state = next_comment

            elif _is_alpha(c):

                symbol = _symbol_token(c, row, column)

                def next_symbol(next_c, next_row, next_column):
                    if _is_alpha(next_c) or _is(_digit, next_c) or _is(_allowed_in_symbol, next_c):
                        symbol.value += next_c
                        return [], None, next_symbol
                    else:
                        return [symbol], next_c, None

                state = next_symbol

            return tokens, None, state

        state = None
        for row, line in enumerate(self._get_lines()):
            for column, char in enumerate(line):
                tokens, char, state = process(char, state, row, column)
                for t in tokens:
                    yield t

        # Flush
        row += 1
        tokens, char, state = process(' ', state, row, 0)
        for t in tokens:
            yield t

        if state:
            raise UnexpectedEnd('Still in state: ' + str(state))
