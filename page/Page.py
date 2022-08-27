from PyNotion import *
from PyNotion.object import *
#from PyNotion.database.Database import Database
from PyNotion.database.Property import *


class Page(BaseObject):
    def __init__(self, bot, page_id, parent=None):
        super().__init__(bot, page_id)
        self.page_url = BaseObject.PageAPI + self.object_id
        self.page_property = self.page_url + "/properties/"
        self.patch_url = f"https://api.notion.com/v1/blocks/{self.object_id}/children"
        self.parent_root = Parent(parent_type=Parent.Type.page, parent_id=self.object_id)
        self.parent = parent

    def retrieve_property_item(self,property_id):
        r = requests.get(url=self.page_property+property_id, headers=self.bot.headers)
        return r.json()

    def retrieve(self, **kwargs):
        return super().retrieve(self.page_url)

    def retrieve_page_data(self):
        # database only
        if not isinstance(self.parent, Database):
            print("can't change to dataframe")
            return False
        r = self.retrieve()
        properties = r['properties']
        result = super().properties_data(properties)
        return result

    def update(self, data, **kwargs):
        return super().update(self.page_url, data)
        # data = data if isinstance(data, str) else json.dumps(data)
        # r = requests.patch(self.page_url, headers=self.bot.patch_headers, data=data)
        # if r.status_code != 200:
        #     print(r.json()['message'])
        # return r.json()

    def update_emoji(self, emoji: str):
        return self.update(Emoji(emoji).make(), )

    def create_page(self, data):
        r = requests.post(Page.PageAPI, headers=self.bot.patch_headers, data=json.dumps(data))
        try:
            return Page(bot=self.bot, page_id=str(r.json()['id']))
        except KeyError:
            print("create failed")
            return r.json()

    def create_database(self, title, properties=None, icon=None, cover=None, is_inline=False):
        template = dict(
            parent=self.parent_root.template,
            title=Text(content=title).template,
            is_inline=is_inline
        )

        if isinstance(properties, dict):
            properties = PropertyObject(properties)
            template.update(dict(properties=properties.make()))

        elif isinstance(properties, PropertyObject):
            template.update(dict(properties=properties.make()))

        else:
            properties = PropertyObject({"UnTitle": TitleProperty()})
            template.update(dict(properties=properties.make()))

        r = requests.post(self.DatabaseAPI, headers=self.bot.patch_headers, data=json.dumps(template))
        return r
        # if r.status_code == 200:
        #     print(f"database {title} 創建成功,id {r.json()['id']} ")
        #     return r.json()
        #
        # else:
        #     print("error", r.json()['message'])
