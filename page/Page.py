from typing import Union
from object import *
import asyncio
import requests


class PageObject(NotionObject):
    def __init__(self, archived=False, **kwargs):
        """
        :param parent: the database parent or page parent. please use Parent object or json format
        :param properties: Properties value of this page. please use Properties object or json format
        :param children: Page content for the new page as an array of block objects. please use Children object or json format
        :param icon: Page icon for the new page. Please use Emoji Object or string emoji.
        :param cover: Page cover for the new page. Please use File Object.
        :param archived: If it is True delete page otherwise restore
        """
        super().__init__()
        params = ['parent', 'properties', 'icon', 'cover', 'children']
        self.template['archived'] = archived
        for key, value in kwargs.items():
            if key in params and value:
                self.template[key] = value.make()


class Page(BaseObject):

    def __init__(self, bot, page_id):
        super().__init__(bot, page_id, 'page')
        self.page_property_api = self.object_api + "/properties/"
        self.update_children_api = f"https://api.notion.com/v1/blocks/{self.object_id}/children"

    def retrieve_property_item(self, property_id):
        r = requests.get(url=self.page_property_api + property_id, headers=self.bot.headers)
        if r.status_code == 200:
            return r.json()
        return r.json()['message']

    def update(self, **kwargs):
        page_object = PageObject(**kwargs)
        r = requests.patch(self.object_api, headers=self.bot.headers, json=page_object.make())
        if r.status_code == 200:
            return r.json()
        return r.json()['message']

    def delete(self):
        return self.update(archived=True)

    def restore(self):
        return self.update(archived=False)

    def create_new_page(self,
                        properties: Properties = Properties(),
                        children: Union[Children, dict] = Children(),
                        icon: Union[Emoji, str] = Emoji('🐧'),
                        cover: Union[File, str] = None):
        page_object = PageObject(
            parent=Parent(self),
            properties=properties,
            children=children,
            icon=icon,
            cover=cover
        )
        r = requests.post(BaseObject.PageAPI, headers=self.bot.headers, json=page_object.make())
        if r.status_code == 200:
            return Page(self.bot, r.json()['id'])
        else:
            return r.json()

    # def create_database(self, title, properties=None, icon=None, cover=None, is_inline=False):
    #     template = dict(
    #         parent=self.parent_root.template,
    #         title=Text(content=title).template,
    #         is_inline=is_inline
    #     )
    #
    #     if isinstance(properties, dict):
    #         properties = PropertyObject(properties)
    #         template.update(dict(properties=properties.make()))
    #
    #     elif isinstance(properties, PropertyObject):
    #         template.update(dict(properties=properties.make()))
    #
    #     else:
    #         properties = PropertyObject({"UnTitle": TitleProperty()})
    #         template.update(dict(properties=properties.make()))
    #
    #     r = requests.post(self.DatabaseAPI, headers=self.bot.patch_headers, data=json.dumps(template))
    #     return r
    # if r.status_code == 200:
    #     print(f"database {title} 創建成功,id {r.json()['id']} ")
    #     return r.json()
    #
    # else:
    #     print("error", r.json()['message'])
