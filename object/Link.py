class Link:
    def __init__(self, url=None):
        self.type = "url"
        self.url = url
        self.template = {"type": self.type, self.type: url}

    def make(self):
        return self.template

    def update(self, url):
        self.url = url
        self.template[self.type] = self.url
