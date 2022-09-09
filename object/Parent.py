from enum import Enum


class Parent:
    class Type(str, Enum):
        database = "database_id"
        page = "page_id"
        workspace = "workspace"

    def __init__(self, parent_type: str, parent_id):
        self.parent_type = parent_type
        self.parent_id = parent_id
        self.template = {'type': self.parent_type, self.parent_type: self.parent_id}

    def make(self) -> dict:
        self.template = {'type': self.parent_type, self.parent_type: self.parent_id}
        return self.template

    def __repr__(self):
        return f"Parent\ntype : {self.parent_type}\nid : {self.parent_id}"