from PyNotion.syntax import *
from PyNotion.object import *


class Property:
    def __init__(self, properties_dict: dict) -> None:
        self.template = {}
        for name, value_type_object in properties_dict.items():
            self.template[name] = value_type_object.make()

    def make(self):
        return self.template


class PropertyBase:
    def __init__(self, prop_type: str):
        self.type = prop_type
        self.template = {self.type: {}}

    def make(self):
        return self.template


class TextProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type="rich_text")


class TitleProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type="title")


class NumberProperty(PropertyBase):
    def __init__(self, _format=Number.Format.number):
        super().__init__(Number.Type.number)
        self.format = _format
        self.template[self.type] = {"format": _format}


class SelectProperty(PropertyBase):
    def __init__(self, *option_list: Select):
        super().__init__(Select.Type.select)
        self.template[self.type] = {"options": [option.make() for option in option_list]}


class MultiSelectProperty(PropertyBase):
    def __init__(self, *option_list):
        super().__init__(Select.Type.multi_select)
        self.template[self.type] = {"options": [{"name": o[0], "color": o[1]} for o in option_list]}


class CheckboxProperty(PropertyBase):
    def __init__(self):
        super().__init__(CheckBox.Type.checkbox)


class DataProperty(PropertyBase):
    def __init__(self):
        super().__init__("date")


class UrlProperty(PropertyBase):
    def __init__(self):
        super().__init__("url")