class Children:
    def __init__(self, *children):
        self.template = {"children": [c.make() for c in children]}

    def make(self):
        return self.template
