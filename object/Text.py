from typing import Union

from .Link import Link
from ..syntax import Colors
from enum import Enum
from PyNotion.database.Property import PropertyBase


class Annotations:
    class Type(str, Enum):
        bold = "bold"
        italic = "italic"
        strikethrough = "strikethrough"
        underline = "underline"
        code = "code"
        color = "color"

    def __init__(self, bold: bool = False, italic: bool = False,
                 strikethrough: bool = False, underline: bool = False,
                 code: bool = False, color=Colors.Text.default):

        self.template = {
                'bold': bold,
                'italic': italic,
                'strikethrough': strikethrough,
                'underline': underline,
                'code': code,
                'color': color
        }

    def make(self):
        return self.template


class Text:
    class Type(str, Enum):
        title = "title"
        rich_text = "rich_text"

    class Filter(str, Enum):
        # "title", "rich_text", "url", "email", and "phone_number"
        # Only return pages where the page property value matches the provided value exactly.
        equals = "equals"
        # Only return pages where the page property value does not match the provided value exactly.
        does_not_equal = "does_not_equal"
        # Only return pages where the page property value contains the provided value.
        contains = "contains"
        # Only return pages where the page property value does not contain the provided value.
        does_not_contain = "does_not_contain"
        # Only return pages where the page property value starts with the provided value.
        starts_with = "starts_with"
        # Only return pages where the page property value ends with the provided value.
        ends_with = "ends_with"
        # Only return pages where the page property value is empty.
        is_empty = "is_empty"
        # Only return pages where the page property value is present.
        is_not_empty = "is_not_empty"

    def __init__(self, content="", annotations=None, link=None):
        self.content = content
        self.link = link
        self.annotations = annotations
        self.template = dict(text={'content': self.content, "link": None})

        if self.link:
            self.link_object = Link(self.link)
            self.template['text']['link'] = self.link_object.template
        if isinstance(self.annotations, Annotations):
            self.template.update(dict(annotations=self.annotations.make()))

    def update_link(self, url):
        self.link = url
        self.link_object.update(self.link)
        self.template[0]['text']["link"] = self.link_object.make()

    def make(self):
        return self.template


class TextProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type="rich_text")


class TitleProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type="title")


class TitleValue(TitleProperty):
    def __init__(self, key, value):
        super().__init__()
        self.value = value
        if isinstance(self.value, str):
            self.value = Text(self.value)

        self.template = {key: [self.value.make()]}


class TextValue(TextProperty):
    def __init__(self, key, value: Union[str, Text]):
        super().__init__()
        self.value = value
        if isinstance(self.value, str):
            self.value = Text(self.value)

        #self.template = {key: {'name': key, self.type: [self.value.make()]}}
        #TODO fix problem
        self.template = {key: [self.value.make()]}