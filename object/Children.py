import json


class Children:
    def __init__(self, *children):
        self.template = [c.make() for c in children]

    def make(self):
        return self.template

    @staticmethod
    def json_template(data):
        if isinstance(data, list):
            data = Children(*data)
        if isinstance(data, Children):
            data = data.make()
        if isinstance(data, dict):
            data = json.dumps(data)
        elif not isinstance(data, str):
            print("Wrong input format")
            raise TypeError

        return data