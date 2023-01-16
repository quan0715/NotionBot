from enum import Enum
from typing import Union


class Parent:
    class Type(str, Enum):
        database = "database_id"
        page = "page_id"
        workspace = "workspace"

    def __init__(self, parent_object: Union['Database', 'Page']):
        self.parent_type = parent_object.parent_type
        self.parent_id = parent_object.object_id
        self.template = {self.parent_type: self.parent_id}

    def make(self) -> dict:
        return self.template

    def __repr__(self):
        return f"Parent type : {self.parent_type}\n object_id : {self.parent_id}"