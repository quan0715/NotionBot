from enum import Enum


class Filter:
    def __init__(self):
        self.template = {}

    def make(self) -> dict:
        return self.template


class PropertyFilter(Filter):
    def __init__(self, prop: str, filter_type: str, condition: str, target):
        super().__init__()
        self.property = prop
        self.filter_type = filter_type
        self.condition = condition
        self.target = target
        self.template = {"property": self.property, self.filter_type: {self.condition: self.target}}


class ConditionFilters(Filter):
    class Operator(str, Enum):
        And = "and"
        Or = "or"

    def __init__(self, operator: Operator, filter_list: list[Filter]):
        super().__init__()
        self.operator = operator
        self.filter_list = filter_list
        self.template = {self.operator: [f.template for f in self.filter_list]}


class SortObject:
    def __init__(self, prop: str, direction="ascending"):
        self.property = prop
        self.direction = direction
        self.template = {
            "property": self.property,
            "direction": self.direction,
        }

    def make(self):
        self.template = {
            "property": self.property,
            "direction": self.direction,
        }
        return self.template


class Query:
    def __init__(self, filters: Filter = None, sorts: list[SortObject] = None,
                 start_cursor: str = None, page_size: int = None):
        self.filters = filters
        self.sorts = sorts
        self.start_cursor = start_cursor
        self.page_size = page_size
        self.template = self.make()

    def make(self) -> dict:
        template = {}
        if self.filters:
            template["filter"] = self.filters.template
        if self.sorts:
            template["sorts"] = [s.make() for s in self.sorts]
        if self.start_cursor:
            template["start_cursor"] = self.start_cursor
        if self.page_size:
            template["page_size"] = self.page_size
        return template
