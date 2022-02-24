

class ChildrenObject:
    pass

class RichTextObject:
      def __init__(self, annotations="default", plain_text="", link=None, href=None, type="text"):
          self.link = link
          self.href = href
          self.plain_text = plain_text
          self.type = type
          self.object_array = [{
              'type': self.type,
              self.type: {'content': self.plain_text, 'link': self.link},
              'annotations': {
                  'bold': False,
                  'italic': False,
                  'strikethrough': False,
                  'underline': False,
                  'code': False,
                  'color': 'default'
              },
            }
          ]

          if annotations != "default":
            self.update_annotations(annotations),

      def update_annotations(self,annotations):
        for key,value in annotations.items():
          self.object_array[0]['annotations'][key] = value

      def update_content(self,word):
            self.plain_text = word
            self.object_array[0][self.type]['content'] = self.plain_text

      def update_link(self,link):
          self.link = link
          self.object_array[0][self.type]['content']['link'] = {'url':self.link}

class PropertyObject:
  def __init__(self) -> None:
      pass
  

class BlockObject:
    def __init__(self,type,traces=None):
        self.type = type
        self.traces = traces
        self.object = self.create_object()
        self.template = self.create_template()

    def create_object(self):
        if self.type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
            if self.traces:
                Object = RichTextObject(**self.traces)
            else:
                Object = RichTextObject()
        else:
            Object = RichTextObject()
        return Object

    def create_template(self):
        Template = {
            "object": "block",
            "type": f"{self.type}",
            f"{self.type}":{}
        }
        if type(self.object) == RichTextObject:
            Template[f"{self.type}"]["text"] = self.object.object_array
        return Template


class Emoji_object:
    template = {"icon": {"type": "emoji", "emoji": ""}}
    def __init__(self,emoji):
        self.emoji = emoji
        Emoji_object.template['icon']['emoji'] = emoji
        self.emoji_json = Emoji_object.template


    def set_emoji(self,emoji):
        self.emoji = emoji
        self.emoji_json['icon']['emoji'] = emoji

    def get_emoji(self):
        return self.emoji

    def get_json(self):
        return self.emoji_json

