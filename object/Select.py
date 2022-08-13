from PyNotion.syntax import *
from enum import Enum


class Select:
    class Type(str, Enum):
        select = "select"
        multi_select = "multi_select"

    class Filter(str, Enum):
        equals = "equals"
        does_not_equal = "does_not_equal"
        is_empty = "is_empty"
        is_not_empty = "is_not_empty"

    def __init__(self, name, color=Colors.Option.default):
        self.name = name
        self.color = color
        self.template = {"name": self.name, "color": self.color}

    def make(self):
        return self.template
