BLOCKSTART = 'blockstart'
BLOCKEND = 'blockend'
STRING = 'string'
NUMBER = 'number'
OPERATOR = 'operator'
SYMBOL = 'symbol'
COMMENT = 'comment'


class Token(object):
    def __init__(self, type, value, row, column):
        self.type = type
        self.value = value
        self.row = row
        self.column = column
