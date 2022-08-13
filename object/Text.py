from .Link import Link
from ..syntax import Colors
from enum import Enum


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


class RichTextObject:
    def __init__(self, annotation: Annotations = Annotations(), plain_text: str = "", href: str = "null"):
        '''
        :param text_feature: dict(bold,italic,strikethrough,underline,code,color->ColorObject)
        :param plain_text: string word of text block
        :param href: string (optional) The URL of any link or internal Notion mention in this text, if any.
        :param type: string "text","mention", "equation".
        '''
        self.href = href
        self.plain_text = plain_text
        self.template = [dict(annotation=annotation.make(), plain_text=self.plain_text, href=href)]


    def update_annotations(self, annotations):
        for key, val in annotations.items():
            if key == 'color':
                self.template[0]['annotations'][key] = val.value
            else:
                self.template[0]['annotations'][key] = val

    def update_plain_text(self, plain_text):
        self.plain_text = plain_text
        self.template[0]['plain_text'] = self.plain_text

    def update_href(self, href):
        self.href = href
        self.template[0]["href"] = self.href


class Text(RichTextObject):
    def __init__(self, annotation=Annotations(), content="", link=""):
        super().__init__(annotation=annotation, plain_text=content, href=link)
        self.content = content
        self.link = link
        self.template[0].update({
            'type': 'text',
            'text': {'content': self.content, "link": None}
        })
        if self.link:
            self.link_object = Link(self.link)
            self.template[0]['text']["link"] = self.link_object.template

    def update_link(self, url):
        self.link = url
        self.link_object.update(self.link)
        self.template[0]['text']["link"] = self.link_object.make()
