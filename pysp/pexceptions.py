# Parsing errors

class ParserError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class SyntaxError(ParserError):
    def __init__(self, message):
        self.message = message


# Runtime errors

class MissingSymbolError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Unable to find symbol:" + self.name

class NoFunctionError(Exception):
    pass