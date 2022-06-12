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

    def get_template(self):
        return self.template

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


class AnnotationsObject:
    def __init__(self, bold=False, italic=False, strikethrough=False, underline=False, code=False,color=Colors.Text.default):
        self.template = {
            'bold': bold,
            'italic': italic,
            'strikethrough': strikethrough,
            'underline': underline,
            'code': code,
            'color': color
        },

    def get_template(self):
        return self.template


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
        self.text_block = text_block

    def get_template(self):
        return self.template

    def update_file(self, file):
        if isinstance(file, str):
            file = FileObject(file)
        if isinstance(file, FileObject):
            self.template[self.block_type] = file.get_template()

    @classmethod
    def rich_text(cls, text_block):
        return {"rich_text": [text.get_template() for text in text_block]}

    @classmethod
    def caption(cls, text_block):
        return {"caption": [text_block.get_template()]}

    def update_color(self, color):
        self.template[self.block_type].update(dict(color=color))

    def update_text(self, text_block):
        if not len(text_block):
            self.text_block = [TextBlockObject(self.default_text)]
        text_block = []
        for i in range(len(self.text_block)):
            if isinstance(self.text_block[i], str):
                text_block.append(TextBlockObject(content=str(self.text_block[i])))
            else:
                text_block.append(self.text_block[i])

        self.template[self.block_type].update(self.rich_text(text_block))

    def update_children(self, children):
        if isinstance(children, list):
            children = ChildrenObject(*children)
        if isinstance(children, ChildrenObject):
            self.template[self.block_type].update(children.get_template())


class LinkObject:
    def __init__(self, link=None):
        self.type = "url"
        self.link = link
        self.template = {"type": self.type, self.type: link}

    def get_template(self):
        return self.template


class FileObject:
    def __init__(self, url, file_type=File.Type.external):
        self.url = url
        self.file_type = file_type
        self.template = dict(type=self.file_type)
        self.template[self.file_type] = (dict(url=self.url))

    def get_template(self):
        return self.template


class EmojiObject:
    def __init__(self, emoji):
        # print(emoji)
        self.emoji = emoji
        self.template = {"type": "emoji", "emoji": self.emoji} if isinstance(self.emoji, str) else None

    def get_template(self) -> dict:
        return self.template


class TextBlockObject(BaseBlockObject):
    def __init__(self, content="This is Text", link=None, annotations=None):
        super().__init__(block_type="text", text_block=None)
        self.content = content
        self.link = link
        self.template[self.block_type] = {"content": self.content}
        if isinstance(link, str):
            self.template[self.block_type].update(dict(link=LinkObject(self.link).template))
        if isinstance(annotations,dict):
            annotations = AnnotationsObject(**annotations)
        if isinstance(annotations, AnnotationsObject):
            self.template.update(annotations=annotations.get_template())


# class RichTextObject:
#     def __init__(self, *text_block: TextBlockObject):
#         self.template =

class ParagraphBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__(block_type="paragraph", color=color, text_block=text_block, children=children)
        self.update_color(self.color)
        self.update_text(self.text_block)
        self.update_children(self.children)


class HeadingBlockObject(BaseBlockObject):
    def __init__(self, heading_level=1, *text_block, color=Colors.Text.default):
        self.heading_level = heading_level
        super().__init__(f"heading_{self.heading_level}", color=color, text_block=text_block)
        self.update_color(self.color)
        self.update_text(self.text_block)
        self.update_children(self.children)


class CalloutBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, emoji=None, children=None):
        super().__init__("callout", color=color, text_block=text_block, children=children)
        self.emoji = emoji
        if isinstance(emoji, str):
            self.template[self.block_type] = dict(icon=EmojiObject(self.emoji).get_template())
        self.update_color(self.color)
        self.update_text(self.text_block)
        self.update_children(children)


class QuoteBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("quote", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.update_color(self.color)
        self.update_text(self.text_block)


class BulletedBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("bulleted_list_item", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.update_color(self.color)
        self.update_text(self.text_block)


class NumberedBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("numbered_list_item", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.update_color(self.color)
        self.update_text(self.text_block)


class ToDoBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, checked=False, children=None):
        super().__init__("to_do", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.update_color(self.color)
        self.update_text(self.text_block)
        self.check = checked
        self.template[self.block_type].update(dict(checked=checked))


class ToggleBlockObject(BaseBlockObject):
    def __init__(self, *text_block, color=Colors.Text.default, children=None):
        super().__init__("toggle", color=color, text_block=text_block, children=children)
        self.update_children(self.children)
        self.update_color(self.color)
        self.update_text(self.text_block)


class CodeBlockObject(BaseBlockObject):
    def __init__(self, *text_block, caption=None, color=Colors.Text.default, language="plain text", children=None):
        super().__init__("code", color=color, text_block=text_block, children=children)
        self.caption = caption
        if isinstance(self.caption, TextBlockObject):
            self.template[self.block_type].update(BaseBlockObject.caption(self.caption))
        self.update_children(self.children)
        self.update_text(self.text_block)
        self.language = language
        self.template[self.block_type].update(dict(language=language))


class ChildPageBlockObject(BaseBlockObject):
    def __init__(self, title="child_page"):
        super().__init__("child_page")
        self.title = title
        self.template[self.block_type] = dict(title=title)


class ChildDataBaseBlockObject(BaseBlockObject):
    def __init__(self, title="child_database"):
        super().__init__("child_database")
        self.title = title
        self.template[self.block_type] = dict(title=title)


class EmbedBlockObject(BaseBlockObject):
    def __init__(self, url):
        super().__init__("embed")
        self.url = url
        self.template[self.block_type] = dict(url=self.url)


class ImageBlockObject(BaseBlockObject):
    def __init__(self, file):
        super().__init__("image")
        self.file = file
        self.update_file(self.file)


class VideoBlockObject(BaseBlockObject):
    def __init__(self, file):
        super().__init__("video")
        self.file = file
        self.update_file(self.file)


class FileBlockObject(BaseBlockObject):
    def __init__(self, file=None):
        super().__init__("file")
        self.file = file
        self.update_file(self.file)


class PDFBlockObject(BaseBlockObject):
    def __init__(self, file):
        super().__init__("pdf")
        self.file = file
        self.update_file(self.file)


class BookmarkBlockObject(BaseBlockObject):
    def __init__(self, caption=None, url=None):
        super().__init__("bookmark")
        self.caption = caption
        self.url = url
        self.template[self.block_type].update(dict(url=self.url))
        if isinstance(self.caption, TextBlockObject):
            self.template[self.block_type].update(BaseBlockObject.caption(self.caption))


class EquationBlockObject(BaseBlockObject):
    def __init__(self, expression):
        super().__init__("equation")
        self.expression = expression
        self.template[self.block_type].update(dict(expression=self.expression))


class DividerBlockObject(BaseBlockObject):
    def __init__(self):
        super().__init__("divider")


class TableOfContentBlockObject(BaseBlockObject):
    # show an outline of content
    def __init__(self, color=Colors.Text.default):
        super().__init__("table_of_contents", color=color)


class BreadcrumbBlockObject(BaseBlockObject):
    def __init__(self):
        super().__init__("breadcrumb")


class ColumnListBlockObject(BaseBlockObject):
    # parent block for column children
    def __init__(self, children=None):
        super().__init__("column_list", children=children)
        self.update_children(self.children)


class ColumnBlockObject(BaseBlockObject):
    def __init__(self, children=None):
        super().__init__("column", children=children)
        self.update_children(self.children)


class LinkPreviewBlockObject(BaseBlockObject):
    # can't be create
    def __init__(self, url=None):
        super().__init__("link_preview")
        self.url = url


class TemplateBlockObject(BaseBlockObject):
    def __init__(self, *title, children=None):
        super().__init__("template", text_block=title, children=children)
        self.update_text(title)
        self.update_children(self.children)


class LinkToPageBlockObject(BaseBlockObject):
    def __init__(self, target):
        # page_id or database_id
        super().__init__("link_to_page")
        if isinstance(target, dict):
            target = ParentObject(target['type'], target['id'])
        if isinstance(target, ParentObject):
            self.template[self.block_type] = target.get_template()


class SyncedBlockObject(BaseBlockObject):
    def __init__(self, synced_from=None, children=None):
        super().__init__("synced_block", children=children)
        self.synced_from = synced_from
        if not self.synced_from:
            self.template[self.block_type].update(dict(synced_from=self.synced_from))
            self.update_children(self.children)
        else:
            self.template[self.block_type].update(dict(synced_from=dict(block_id=self.synced_from)))


class TableBlockObject(BaseBlockObject):
    def __init__(self, table_width=1, column_header=True, row_header=True, children=None):
        super().__init__("table", children=children)
        self.table_width = table_width
        self.column_header = column_header
        self.row_header = row_header
        self.update_children(self.children)
        self.template[self.block_type].update(
            dict(
                table_width=self.table_width,
                has_column_header=self.column_header,
                has_row_header=self.row_header,
            )
        )
        row_list = self.template[self.block_type]["children"]
        for row in row_list:
            cells = row['table_row']['cells']
            for i in range(self.table_width - len(cells)):
                row['table_row']['cells'].append([TextBlockObject("").get_template()])


class TableRowBlockObject(BaseBlockObject):
    def __init__(self, *cells):
        super().__init__("table_row")
        cell_list = []
        for cell in cells:
            if isinstance(cell, str):
                cell = TextBlockObject(content=cell)
            if isinstance(cell, TextBlockObject):
                cell_list.append([cell.get_template()])

        self.template[self.block_type].update(dict(cells=cell_list))


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
    Embed = EmbedBlockObject
    Image = ImageBlockObject
    Video = VideoBlockObject
    PDF = PDFBlockObject
    Bookmark = BookmarkBlockObject
    Equation = EquationBlockObject
    Divider = DividerBlockObject
    File = FileBlockObject
    TableOfContent = TableOfContentBlockObject
    Breadcrumb = BreadcrumbBlockObject
    ColumnList = ColumnListBlockObject
    ColumnBlock = ColumnBlockObject
    Template = TemplateBlockObject
    LinkToPage = LinkToPageBlockObject
    Synced = SyncedBlockObject
    TableRow = TableRowBlockObject
    Table = TableBlockObject


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
