from .Property import *
from PyNotion.object import *


# class TitleValue(TitleProperty):
#     def __init__(self, key, value):
#         super().__init__()
#         self.value = value
#         if isinstance(self.value, str):
#             self.value = Text(self.value)
#
#         self.template = {key: {self.type: self.value.make()}}
#
#
# class TextValue(TextProperty):
#     def __init__(self, key, value):
#         super().__init__()
#         self.value = value
#         if isinstance(self.value, str):
#             self.value = Text(self.value)
#
#         self.template = {key: {self.type: self.value.make()}}

#
# class NumberValue(NumberProperty):
#     def __init__(self, key, value):
#         super().__init__()
#         self.value = value
#         if isinstance(self.value, int) or isinstance(self.value, float):
#             self.value = Number(self.value)
#
#         self.template = {key: {self.type: self.value.make()}}
#

# class SelectValue(SelectProperty):
#     def __init__(self, key, value):
#         super().__init__()
#         self.value = value
#         if isinstance(self.value, str):
#             self.value = Option(self.value)
#
#         self.value.value()
#         self.template = {key: {self.type: self.value.make()}}
#
#
# class MultiSelectValue(MultiSelectProperty):
#     def __init__(self, key, value: list):
#         super().__init__()
#         self.value = value
#         self.option_list = []
#         for p in self.value:
#             if isinstance(p, str):
#                 o = Option(p)
#                 o.value()
#                 self.option_list.append(o.make())
#
#             elif isinstance(p, Option):
#                 p.value()
#                 self.option_list.append(p.make())
#         self.template = {key: {self.type: self.option_list}}


# class CheckboxValue(CheckboxProperty):
#     def __init__(self, key, value):
#         super().__init__()
#         self.value = value
#
#         self.template = {key: {self.type: self.value}}

