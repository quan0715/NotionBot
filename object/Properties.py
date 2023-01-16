import json
from . import *
from . import NotionObject


class Properties(NotionObject):
    def __init__(self, **kwargs):
        super().__init__()

        for k, v in kwargs.items():
            if isinstance(v, NotionObject):
                self.template.update({k: v.make()})
            else:
                self.template.update({k: v})