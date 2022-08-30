from PyNotion import *
from .Children import Children
import aiohttp
import asyncio


class BaseObject:
    BlockAPI = "https://api.notion.com/v1/blocks/"
    DatabaseAPI = "https://api.notion.com/v1/databases/"
    PageAPI = 'https://api.notion.com/v1/pages/'

    def __init__(self, bot, object_id):
        self.bot = bot
        self.object_id = object_id

    def retrieve(self, url):
        r = requests.get(url, headers=self.bot.headers)
        return r.json()

    def update(self, url, data):
        data = data if isinstance(data, str) else json.dumps(data)
        r = requests.patch(url, headers=self.bot.patch_headers, data=data)
        if r.status_code != 200:
            print(r.json()['message'])
        return r.json()

    def delete_object(self):
        url = self.__class__.BlockAPI + self.object_id
        r = requests.delete(url, headers=self.bot.headers)
        return r.json()

    def retrieve_children(self):
        url = BaseObject.BlockAPI + self.object_id + "/children"
        r = requests.get(url, headers=self.bot.headers)
        return r.json()

    def append_children(self, data):
        try:
            data = Children.json_template(data)
        except TypeError:
            raise TypeError
        # # list of children
        # # ChildrenObject
        # # dict
        # if isinstance(data, list):
        #     data = Children(*data)
        # if isinstance(data, Children):
        #     data = data.make()
        # if isinstance(data, dict):
        #     data = json.dumps(data)
        # elif not isinstance(data, str):
        #     print("Wrong input format")
        #     #data = json.dumps(data.get_template())
        url = BaseObject.BlockAPI + self.object_id + "/children"
        r = requests.patch(url, headers=self.bot.patch_headers, data=data)
        if r.status_code != 200:
            return r.json()['message']
        else:
            return r.json()['results']

    async def async_append_children(self, data, session):
        try:
            data = Children.json_template(data)
        except TypeError:
            raise TypeError
        url = BaseObject.BlockAPI + self.object_id + "/children"
        async with session.patch(url, headers=self.bot.patch_headers, data=data) as resp:
            await asyncio.sleep(0.4)
            print(resp.status)
            print(await resp.text())


        # if r.status_code != 200:
        #     return r.json()['message']
        # else:
        #     return r.json()['results']
        # return r

    @classmethod
    def properties_data(cls, json_data):
        result = {}
        for key, value in json_data.items():
            prop_type = value['type']
            try:
                if prop_type in ['title', 'rich_text']:
                    result[key] = value[prop_type][0]['plain_text']
                elif prop_type in ['number', 'url']:
                    result[key] = value[prop_type]
                elif prop_type == 'select':
                    result[key] = value[prop_type]['name']
                elif prop_type == 'date':
                    text = value[prop_type]['start']
                    if value[prop_type]['end']:
                        text += f" ~ {value[prop_type]['end']}"
                    # if value[prop_type]['start']
                    result[key] = text
                elif prop_type == 'people':
                    result[key] = ""
                    # print(value[prop_type])
                    for n in value[prop_type]:
                        result[key] += f"{n['name']} "
                else:
                    result[key] = "None"
            except:
                result[key] = "None"
        return result
