
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
          'href': self.href
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
    
    
class PropertyObject:
  def __init__(self) -> None:
      pass
  
