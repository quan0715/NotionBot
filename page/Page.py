from PyNotion import *
from PyNotion.object import *
import aiohttp
import asyncio
#from PyNotion.database.Database import Database
from PyNotion.database.Property import *


class Page(BaseObject):
    object = "page"

    @classmethod
    def page_object(cls, parent: Parent, prop_value: PropertyValue, children: Children, icon: Emoji, cover: File):
        r = dict(parent=parent.make(), archived=False)
        r.update(prop_value.make())
        if children:
            r.update(children.make())
        if icon:
            r['icon'] = icon.make()
        if cover:
            r['cover'] = cover.make()

        return r

    def __init__(self, bot, page_id, parent=None):
        super().__init__(bot, page_id)
        self.page_url = BaseObject.PageAPI + self.object_id
        self.page_property = self.page_url + "/properties/"
        self.patch_url = f"https://api.notion.com/v1/blocks/{self.object_id}/children"
        self.details: dict = self.retrieve()
        self.created_by: dict = self.details['created_by']
        self.last_edited_by: dict = self.details['last_edited_by']
        self.url = self.details['url']
        self.last_edited_time = self.details['last_edited_time']
        self.archived = self.details['archived']
        self.parent = self.get_parent()
        self.properties = self.details['properties']

    def __repr__(self):
        return f"""------------------------------------------------------
{self.parent}
------------------------------------------------------
Object : {self.object} 
id : {self.object_id}
------------------------------------------------------
created_by : {self.created_by}
last_edited_by : {self.last_edited_by}
last_edited_time : {self.last_edited_time}
------------------------------------------------------
archive : {self.archived}
url : {self.page_url}
------------------------------------------------------
"""

    def print_properties(self):
        r = [f"\t{k} --- {v['type']} --- {v['id']}" for k,v in self.properties.items()]
        return "\n".join(r)

    def get_parent(self):
        return Parent(
            parent_type=self.details['parent']['type'],
            parent_id=self.details['parent'][self.details['parent']['type']]
        )

    def retrieve_property_item(self,property_id):
        r = requests.get(url=self.page_property+property_id, headers=self.bot.headers)
        return r.json()

    def retrieve(self, **kwargs):
        return super().retrieve(self.page_url)

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


class PageObject:
    def __init__(self, parent: Parent, prop_value: PropertyValue, children: Children, icon: Emoji, cover: File):
        self.template = dict(parent=parent.make(), archived=False)
        self.template.update(prop_value.make())
        if children:
            self.template.update(children.make())
        if icon:
            self.template['icon'] = icon.make()
        if cover:
            self.template['cover'] = cover.make()

    def make(self):
        return self.template