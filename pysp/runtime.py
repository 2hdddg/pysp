
class Type(object):
    def __init__(self, name):
        self.typename = name


class Number(object):
    def __init__(self, value):
        self.value = int(value)
        self.type = Type('number')

    def __str__(self):
        return repr(self.value)
