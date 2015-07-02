class Tokenizer(object):
    def __init__(self,  input):
        self._input = input

    def begin(self):
        pass

    def _get_lines(self):
        return self._input.splitlines(True)

    def get_tokens(self):
        def is_block_start(c):
            return c in ('(')

        def is_block_end(c):
            return c in (')')

        def is_operator(c):
            return c in ('+', '-', '*', '/')

        def is_string_start(c):
            return c in ('"', "'")

        def is_line_comment_start(c):
            return c in (';')

        def is_multiline_comment_start(c):
            return c in ('`')

        def is_whitespace(c):
            return c in (' ', '\t', '\n')

        def is_digit(c):
            return c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

        def is_decimal(c):
            return c in ('.')

        def token(type, value, row, column):
            return {
                'type': type,
                'value': value,
                'row': row,
                'column': column
            }

        def blockstart_token(block, row, column):
            return token('blockstart', block, row, column)

        def blockend_token(block, row, column):
            return token('blockend', block, row, column)

        def string_token(contents, row, column):
            return token('string', contents, row, column)

        def number_token(number, row, column):
            return token('number', number, row, column)

        def operator_token(operator, row, column):
            return token('operator', operator, row, column)

        def symbol_token(symbol, row, column):
            return token('symbol', symbol, row, column)

        def comment_token(comment, row, column):
            return token('comment', comment, row, column)

        def next(c, state, row, column):
            if state:
                return next_with_state(c, state, row, column)
            else:
                return next_no_state(c, row, column)

        def next_with_state(c, state, row, column):
            token = state['token']
            state_row = state['row']
            state_column = state['column']

            in_string = state.get('in_string', False)
            if in_string:
                string_start = state['string_start']
                if c == string_start:
                    return [string_token(token, state_row, state_column)], None
                token += c
                state['token'] = token
                return [], state

            in_number = state.get('in_number', False)
            if in_number:
                if is_digit(c):
                    token += c
                    state['token'] = token
                    return [], state
                if is_decimal(c):
                    has_decimal = state.get('has_decimal', False)
                    if has_decimal:
                        raise "hell"
                    state['has_decimal'] = True
                    token += c
                else:
                    number = number_token(token, state_row, state_column)
                    tokens, state = next_no_state(c, row, column)
                    tokens.insert(0, number)
                    return tokens, state

            in_comment = state.get('in_comment', False)
            if in_comment:
                is_line_comment = state['line_comment']
                if is_line_comment:
                    if row > state_row:
                        comment = comment_token(token, state_row, state_column)
                        tokens, state = next_no_state(c, row, column)
                        tokens.insert(0, comment)
                        return tokens, state
                else:
                    comment_end = state['comment_start']
                    if c == comment_end:
                        return [comment_token(token, state_row, state_column)], None
                token += c
                state['token'] = token
                return [], state

            if is_whitespace(c):
                return [symbol_token(token, state_row, state_column)], None

            if is_operator(c):
                return [symbol_token(token, state_row, state_column), operator_token(c, row, column)], None

            if is_block_start(c):
                return [symbol_token(token, state_row, state_column), blockstart_token(c, row, column)], None

            if is_block_end(c):
                return [symbol_token(token, state_row, state_column), blockend_token(c, row, column)], None

            token += c
            state['token'] = token
            return [], state

        def next_no_state(c, row, column):
            if is_whitespace(c):
                return [], None

            if is_operator(c):
                return [operator_token(c, row, column)], None

            if is_block_start(c):
                return [blockstart_token(c, row, column)], None

            if is_block_end(c):
                return [blockend_token(c, row, column)], None

            if is_string_start(c):
                return [], {
                    'in_string': True,
                    'string_start': c,
                    'token': '',
                    'row': row,
                    'column': column
                }

            if is_digit(c):
                return [], {
                    'in_number': True,
                    'token': c,
                    'row': row,
                    'column': column
                }

            if is_line_comment_start(c):
                return [], {
                    'in_comment': True,
                    'comment_start': c,
                    'line_comment': True,
                    'token': '',
                    'row': row,
                    'column': column
                }

            if is_multiline_comment_start(c):
                return [], {
                    'in_comment': True,
                    'comment_start': c,
                    'line_comment': False,
                    'token': '',
                    'row': row,
                    'column': column
                }

            return [], {
                'token': c,
                'row': row,
                'column': column
            }

        state = None
        for row, line in enumerate(self._get_lines()):
            for column, char in enumerate(line):
                tokens, state = next(char, state, row, column)
                for t in tokens:
                    yield t

        # Flush
        row += 1
        tokens, next_state = next(' ', state, row, 0)
        if next_state:
            print "Error near:" + state['token']
            print "State is: " + str(state)
            print "Next state is: " + str(next_state)
            raise "hell"
        for t in tokens:
            yield t

    def end(self):
        pass

if __name__ == "__main__":
    example = '''
        ; Comment
        (12+1)
    a b c
    'string'
    ` a
    multiline
    comment!`
    '''

    tokenizer = Tokenizer(example)
    for x in tokenizer.get_tokens():
        print x
