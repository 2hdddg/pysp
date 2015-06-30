import runtime


class Runner(object):
    def __init__(self, ast):
        self._ast = ast

    def run(self):
        scope = runtime.Scope()
        return scope.execute(self._ast)


if __name__ == "__main__":
    from tokenizer import Tokenizer
    from parser import Parser

    def get_ast(code):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)
        return parser.get_ast()

    def print_result(code):
        ast = get_ast(code)
        result = Runner(ast).run()
        print "Code:"
        print code
        print "Output:"
        print result

    code = '''
        (+ 2 2)
    '''
    print_result(code)

    code = '''
        2
    '''
    print_result(code)

    code = '''
        2 3
    '''
    print_result(code)

    code = '''
        'string'
    '''
    print_result(code)

    code = '''
        (1)
    '''
    #print_result(code)
