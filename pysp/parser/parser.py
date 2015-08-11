from pysp.tokenizer import token


class Parser(object):
    def __init__(self, tokens):
        self._tokens = tokens

    def _next_token(self):
        try:
            return self._tokens.next()
        except StopIteration:
            return None

    def _begin(self):
        t = self._next_token()
        sexp = []
        while t:
            if t.type == token.BLOCKSTART:
                sexp.append(self._begin())
            if t.type == token.BLOCKEND:
                return sexp
            elif t.type in (token.STRING, token.NUMBER, token.OPERATOR, token.SYMBOL):
                sexp.append(t)
            elif t.type == token.COMMENT:
                pass

            t = self._next_token()

        return sexp

    def parse(self):
        root = self._begin()
        return root
