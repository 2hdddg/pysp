from parser import Atom, Node, Symbol
from pexceptions import MissingSymbolError


class StackFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.result = None

symbols = {
    '+': { 'x': 1}
}

"""
    (define id expr)
        (define pi 3.14)
        (define salutation (list-ref '("Hi" "Hello") (random 2)))

    (define id (lambda (arg ...) body ...))

    (define (id arg ...) body ...)
        (define (greet name)
          (string-append salutation ", " name))
"""

class Runner(object):
    def __init__(self, ast):
        self._ast = ast

    def run(self):
        def find_symbol(frame, name):
            symbol = symbols.get(name, None)
            if not symbol:
                raise MissingSymbolError(name)

        def evaluate_symbol(frame, name):
            symbol = find_symbol(frame, name)

        def evaluate(frame, node):
            for child in node.get_children():
                if isinstance(child, Atom):
                    frame.result = child.get_runtime_instance()

                if isinstance(child, Node):
                    next_frame = StackFrame(frame)
                    evaluate(next_frame, child)
                    frame.result = next_frame.result

                if isinstance(child, Symbol):
                    evaluate_symbol(frame, child.value)
                    #symbol = find_symbol(frame, child.value)

        frame = StackFrame(None)
        evaluate(frame, self._ast)
        return frame.result


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
