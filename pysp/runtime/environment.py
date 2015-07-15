class Environment(object):
    def __init__(self, bindings={}, parent=None):
        self.bindings = bindings
        self.parent = parent

    def nest(self):
        return Environment(parent=self)

    def get_binding(self, name):
        if name in self.bindings:
            return self.bindings[name]

        if self.parent:
            return self.parent.get_binding(name)

        # Raise instead?
        return None

    def bind(self, name, value):
        self.bindings[name] = value
