import json


class PropertyValue:
    def __init__(self, *values):
        self.template = {'properties': {}}

        for p in values:
            self.template['properties'].update(p.make())

    def make(self):
        return self.template

    @staticmethod
    def json_template(data):
        if isinstance(data, list):
            data = PropertyValue(*data)
        if isinstance(data, PropertyValue):
            data = data.make()
        if isinstance(data, dict):
            data = json.dumps(data)
        if not isinstance(data, str):
            print("Wrong input format")
            raise TypeError
        return data