
ROOT = 'root'
LAMBDA = 'lambda'
PARAMETER = 'parameter'
BODY = 'body'
STRING = 'string'
NUMBER = 'number'
SYMBOL = 'symbol'
APPLICATION = 'application'
DEFINITION = 'definition'
QUOTE = 'quote'


class Node(object):
    def __init__(self, type, value=None):
        self.type = type
        self.children = []
        self.value = value

    def add(self, node):
        self.children.append(node)

    def show(self, indent=0):
        me = self.type
        if self.value:
            me = me + '(' + str(self.value) + ')'
        print (indent * " ") + me
        for child in self.children:
            child.show(indent + 1)
