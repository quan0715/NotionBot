from enum import Enum


class File:
    class Type(str, Enum):
        file = "file"
        external = "external"

    def __init__(self, url, file_type=Type.external):
        self.url = url
        self.file_type = file_type
        self.template = dict(type=self.file_type)
        self.template[self.file_type] = (dict(url=self.url))

    def make(self) -> dict:
        return self.template