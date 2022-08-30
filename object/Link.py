from enum import Enum
from PyNotion.database.Property import PropertyBase


class Url:
    def __init__(self, url:str):
        self.url = url

    def make(self):
        return self.url


class UrlProperty(PropertyBase):
    def __init__(self):
        super().__init__("url")


class UrlValue(UrlProperty):
    def __init__(self, key, value):
        super().__init__()
        self.value = value
        if isinstance(self.value, str):
            self.value = Url(self.value)
        self.template = {key: {self.type: self.value.make()}}


class Link(UrlProperty):
    def __init__(self, url=None):
        super().__init__()
        self.url = url
        self.template = {"type": self.type, self.type: url}

    def make(self):
        return self.template

    def update(self, url):
        self.url = url
        self.template[self.type] = self.url