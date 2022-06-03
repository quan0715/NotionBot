from enum import Enum
from PyNotion.syntax import *


class PropertyFilter:
    def __init__(self, prop: str, filter_type: str, condition: str, target):
        self.property = prop
        self.filter_type = filter_type
        self.condition = condition
        self.target = target
        self.template = {"property": self.property, self.filter_type: {self.condition: self.target}}


class ConditionFilters:
    def __init__(self, operator, filter_list):
        self.operator = operator
        self.filter_list = filter_list
        self.template = {self.operator: [f.template for f in self.filter_list]}


class Sorts:
    def __init__(self, sort_list: list):
        self.template = [t.template for t in sort_list]


class SortObject:
    def __init__(self, prop, direction="ascending"):
        self.property = prop
        self.direction = direction
        self.template = {
            "property": self.property,
            "direction": self.direction,
        }


class Query:
    def __init__(self, filters=None, sorts: Sorts = None, start_cursor: str = None, page_size: int = None):
        self.filters = filters
        self.sorts = sorts
        self.start_cursor = start_cursor
        self.page_size = page_size
        self.template = self.make_template()

    def make_template(self):
        template = {}
        if self.filters:
            template["filter"] = self.filters.template
        if self.sorts:
            template["sorts"] = self.sorts.template
        if self.start_cursor:
            template["start_cursor"] = self.start_cursor
        if self.page_size:
            template["page_size"] = self.page_size
        return template


class Option:
    def __init__(self, name, color=Colors.Option.default):
        self.name = name
        self.color = color
        self.template = {"name": self.name, "color": self.color}

    def get_template(self):
        return self.template


class ParentObject:
    def __init__(self, parent_type: str, parent_id):
        self.parent_type = parent_type
        self.parent_id = parent_id
        self.template = {'type': self.parent_type, self.parent_type: self.parent_id}

    def make_template(self):
        self.template = {'type': self.parent_type, self.parent_type: self.parent_id}


class ChildrenObject:
    def __init__(self, *children):
        self.template = {"children": [a.get_template() for a in children]}

    def get_template(self):
        return self.template


class PropertyBase:
    def __init__(self, prop_type: str):
        self.type = prop_type
        self.template = {self.type: {}}


class TextProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type=Text.Type.rich_text)


class TitleProperty(PropertyBase):
    def __init__(self):
        super().__init__(prop_type=Text.Type.title)


class NumberProperty(PropertyBase):
    def __init__(self, _format=Number.Format.number):
        super().__init__(Number.Type.number)
        self.format = _format
        self.template[self.type] = {"format": _format}


class SelectProperty(PropertyBase):
    def __init__(self, *option_list: Option):
        super().__init__(Select.Type.select)
        self.template[self.type] = {"options": [option.get_template() for option in option_list]}


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


class RichTextObject:
    def __init__(self, text_feature: dict = None, plain_text: str = "", href: str = ""):
        '''
        :param text_feature: dict(bold,italic,strikethrough,underline,code,color->ColorObject)
        :param plain_text: string word of text block
        :param href: string (optional) The URL of any link or internal Notion mention in this text, if any.
        :param type: string "text","mention", "equation".
        '''
        self.href = href
        self.plain_text = plain_text
        self.template = [{
            # 'type': "",
            # self.type: {'content': self.plain_text},
            'annotations': {
                'bold': False,
                'italic': False,
                'strikethrough': False,
                'underline': False,
                'code': False,
                'color': Colors.Text.default
            },
            "plain_text": self.plain_text,
            "href": self.href if self.href else "null"
        }]
        if text_feature:
            self.update_annotations(text_feature),

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


class TextObject(RichTextObject):
    def __init__(self, text_feature=None, content="", link=None):
        super().__init__(text_feature=text_feature, plain_text=content, href=link)
        self.content = content
        self.link = link
        self.template[0].update({
            'type': 'text',
            'text': {'content': self.content, "link": None}
        })
        if self.link:
            self.link_object = LinkObject(self.link)
            self.template[0]['text']["link"] = self.link_object.template

    def update_link(self, url):
        self.link = url
        self.link_object.set_url(self.link)
        self.template[0]['text']["link"] = self.link_object.template


class PropertyObject:
    def __init__(self, properties_dict: dict) -> None:
        self.template = {}
        for name, value_type_object in properties_dict.items():
            self.template[name] = value_type_object.template

    def get_template(self):
        return self.template



class BaseBlockObject:
    def __init__(self, block_type, color=Colors.Text.default, text_block=None, children=None):
        self.block_type = block_type
        self.template = {"type": self.block_type, self.block_type: {}}
        self.color = color
        self.children = children
        self.default_text = f"{self.block_type}"
        if not isinstance(self, TextBlockObject):
            self.text_block = text_block if text_block else [TextBlockObject(self.default_text)]
            self.template[self.block_type] = self.rich_text(self.text_block)
            if not isinstance(self,CodeBlockObject):
                self.template[self.block_type].update(dict(color=self.color))

    def get_template(self):
        return self.template

    @classmethod
    def rich_text(cls, text_block):
        return {"rich_text": [text.get_template() for text in text_block]}

    @classmethod
    def caption(cls, text_block):
        return {"caption": [text_block.get_template()]}

    def update_children(self, children):
        if isinstance(children, ChildrenObject):
            self.template[self.block_type].update(children.get_template())


class LinkObject:
    def __init__(self,link=None):
        self.type = "url"
        self.link = link
        self.template = {"type":self.type,self.type:link}

    def get_template(self):
        return  self.template


class TextBlockObject(BaseBlockObject):
    def __init__(self, content="This is Text", link=None):
        super().__init__(block_type="text", text_block=None)
        self.content = content
        self.link = link
        self.template[self.block_type] = {"content": self.content}
        if isinstance(link, str):
            self.template[self.block_type].update(dict(link=LinkObject(self.link).template))


# class RichTextObject:
#     def __init__(self, *text_block: TextBlockObject):
#         self.template =

class ParagraphBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__(block_type="paragraph", color=color, text_block=text_block,children=children)
        self.update_children(children)


class HeadingBlockObject(BaseBlockObject):
    def __init__(self, heading_level=1, *text_block, color=Colors.Text.default):
        self.heading_level = heading_level
        super().__init__(f"heading_{self.heading_level}", color=color, text_block=text_block)


class EmojiObject:
    def __init__(self, emoji):
        #print(emoji)
        self.emoji = emoji
        self.template = {"type": "emoji", "emoji": self.emoji} if isinstance(self.emoji, str) else None


    def get_template(self) -> dict:
        return self.template


class CalloutBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, emoji=None, children=None):
        super().__init__("callout", color=color, text_block=text_block,children=children)
        self.emoji = emoji
        if isinstance(emoji, str):
            self.template[self.block_type] = dict(icon=EmojiObject(self.emoji).get_template())
        self.update_children(children)


class QuoteBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("quote", color=color, text_block=text_block, children=children)
        self.update_children(self.children)


class BulletedBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("bulleted_list_item", color=color, text_block=text_block, children=children)
        self.update_children(self.children)


class NumberedBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("numbered_list_item", color=color, text_block=text_block, children=children)
        self.update_children(self.children)


class ToDoBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, checked=False, children=None):
        super().__init__("to_do", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.check = checked
        self.template[self.block_type].update(dict(checked=checked))


class ToggleBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("toggle", color=color, text_block=text_block, children=children)
        self.update_children(self.children)


class CodeBlockObject(BaseBlockObject):
    def __init__(self, *text_block, caption=None, color=Colors.Text.default, language="plain text", children=None):
        super().__init__("code", color=color, text_block=text_block, children=children)
        self.caption = caption
        if isinstance(self.caption, TextBlockObject):
            self.template[self.block_type].update(BaseBlockObject.caption(self.caption))
        self.update_children(self.children)
        self.language = language
        self.template[self.block_type].update(dict(language=language))


class ChildPageBlock(BaseBlockObject):
    def __init__(self, title="child_page"):
        super().__init__("child_page")
        self.title = title
        self.template[self.block_type] = dict(title=title)


class ChildDataBaseBlock(BaseBlockObject):
    def __init__(self, title="child_database"):
        super().__init__("child_database")
        self.title = title
        self.template[self.block_type] = dict(title=title)


class Blocks:
    Paragraph = ParagraphBlockObject
    Heading = HeadingBlockObject
    Code = CodeBlockObject
    Toggle = ToggleBlockObject
    Numbered = NumberedBlockObject
    Bulleted = BulletedBlockObject
    ToDoList = ToDoBlockObject
    Callout = CalloutBlockObject
    Quote = QuoteBlockObject
    Text = TextBlockObject



class BlockObject:
    def __init__(self, block_type, traces=None, Children=None):
        self.object = None
        self.block_type = block_type
        self.traces = traces
        self.template = {}
        self.create_object()
        self.create_template()

    def create_object(self):
        if self.block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
            if self.traces:
                self.object = TextObject(**self.traces)
            else:
                self.object = TextObject()

    def create_template(self):
        self.template = {
            "object": "block",
            "type": f"{self.block_type}",
            f"{self.block_type}": {}
        }
        if type(self.object) == TextObject:
            self.template[f"{self.block_type}"]["text"] = self.object.template



class EmojiObject:
    template = {"icon": {"type": "emoji", "emoji": ""}}

    def __init__(self, emoji):
        self.emoji = emoji
        EmojiObject.template['icon']['emoji'] = emoji
        self.emoji_json = EmojiObject.template

    def set_emoji(self, emoji):
        self.emoji = emoji
        self.emoji_json['icon']['emoji'] = emoji

    def get_emoji(self):
        return self.emoji

    def get_json(self):
        return self.emoji_json


class LinkObject:
    def __init__(self, url: str = ""):
        self.url = ""
        self.template = {}
        if url:
            self.set_url(url)

    def set_url(self, url: str):
        """
        :type url: str
        """
        self.url = url
        self.template = {"type": "url", "url": self.url}
