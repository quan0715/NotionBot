class NotionObject:
    def __init__(self):
        self.template = {}

    def make(self):
        return self.template


class PropertyObject(NotionObject):
    def __init__(self, properties_dict: dict) -> None:
        super().__init__()
        for name, value_type_object in properties_dict.items():
            self.template[name] = value_type_object.make()


class PropertyName(NotionObject):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.template = dict(name=name)


class PropertyBase(NotionObject):
    def __init__(self, prop_type: str):
        NotionObject.__init__(self)
        self.type = prop_type
        self.template.update({self.type: dict()})

    def post(self, data):
        return {self.type: data.make()}
