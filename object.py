from enum import Enum


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


class TextColor(Enum):
    default = "default"
    gray = "gray"
    brown = "brown"
    orange = "orange"
    yellow = "yellow"
    green = "green"
    blue = "blue"
    purple = "purple"
    pink = "pink"
    red = "red"


class BackgroundColor(Enum):
    gray = "gray_background"
    brown = "brown_background"
    orange = "orange_background"
    yellow = "yellow_background"
    green = "green_background"
    blue = "blue_background"
    purple = "purple_background"
    pink = "pink_background"
    red = "red_background"


class ChildrenObject:
    pass


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
        self.object_array = [{
            # 'type': "",
            # self.type: {'content': self.plain_text},
            'annotations': {
                'bold': False,
                'italic': False,
                'strikethrough': False,
                'underline': False,
                'code': False,
                'color': TextColor.default.value
            },
            "plain_text": self.plain_text,
            "href": self.href if self.href else "null"
        }]
        if text_feature:
            self.update_annotations(text_feature),

    def update_annotations(self, annotations):
        for key, val in annotations.items():
            if key == 'color':
                self.object_array[0]['annotations'][key] = val.value
            else:
                self.object_array[0]['annotations'][key] = val

    def update_plain_text(self, plain_text):
        self.plain_text = plain_text
        self.object_array[0]['plain_text'] = self.plain_text

    def update_href(self, href):
        self.href = href
        self.object_array[0]["href"] = self.href


class TextObject(RichTextObject):
    def __init__(self, text_feature=None, content="", link=None):
        super().__init__(text_feature=text_feature, plain_text=content, href=link)
        self.content = content
        self.link = link
        self.object_array[0].update({
            'type': 'text',
            'text': {'content': self.content, "link": None}
        })
        if self.link:
            self.link_object = LinkObject(self.link)
            self.object_array[0]['text']["link"] = self.link_object.template

    def update_link(self, url):
        self.link = url
        self.link_object.set_url(self.link)
        self.object_array[0]['text']["link"] = self.link_object.template


class PropertyObject:
    def __init__(self) -> None:
        pass


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
            self.template[f"{self.block_type}"]["text"] = self.object.object_array



class Emoji_object:
    template = {"icon": {"type": "emoji", "emoji": ""}}

    def __init__(self, emoji):
        self.emoji = emoji
        Emoji_object.template['icon']['emoji'] = emoji
        self.emoji_json = Emoji_object.template

    def set_emoji(self, emoji):
        self.emoji = emoji
        self.emoji_json['icon']['emoji'] = emoji

    def get_emoji(self):
        return self.emoji

    def get_json(self):
        return self.emoji_json
