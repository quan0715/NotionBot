
from page import *
from object import *
import asyncio
import requests
from typing import Union


class DatabaseObject(NotionObject):
    def __init__(self, archived=False, **kwargs):
        """
        :param parent: the database parent or page parent. please use Parent object or json format
        :param properties: Properties value of this page. please use Properties object or json format
        :param icon: Page icon for the new page. Please use Emoji Object or string emoji.
        :param cover: Page cover for the new page. Please use FileValue Object.
        :param archived: If it is True delete page otherwise restore\
        :param title: If it is True delete page otherwise restore
        """
        super().__init__()
        # self.template.update(title.make())
        params = ['parent', 'properties', 'icon', 'cover', 'title','description']
        self.template['archived'] = archived
        for key, value in kwargs.items():
            if key in params and value:
                self.template[key] = value.make()


class DatabaseDescription(NotionObject):
    def __init__(self, *description: Union[str, Text]):
        super().__init__()
        description = TextValue(*description).make()
        self.template = description['rich_text']


class DatabaseTitle(NotionObject):
    def __init__(self, *contents):
        super().__init__()
        title = TextValue(*contents).make()
        self.template = title['rich_text']


class Database(BaseObject):
    def __init__(self, bot, database_id: str):
        super().__init__(bot, database_id, 'database')
        self.database_query_api = f'{self.object_api}/query'
        self.description = None

    def update(self, **kwargs):
        database_object = DatabaseObject(**kwargs)
        r = requests.patch(self.object_api, headers=self.bot.headers, json=database_object.make())
        if r.status_code == 200:
            return r.json()
        return r.json()['message']

    def create_new_page(self,
                        properties: Properties = Properties(),
                        children: Union[Children, dict] = Children(),
                        icon: Union[Emoji, str] = Emoji('🐧'),
                        cover: Union[FileValue, str] = None):
        database_object = DatabaseObject(
            parent=Parent(self),
            properties=properties,
            children=children,
            icon=icon,
            cover=cover
        )
        # print(database_object.make())
        r = requests.post(BaseObject.PageAPI, headers=self.bot.headers, json=database_object.make())
        if r.status_code == 200:
            return Page(bot=self.bot, page_id=str(r.json()['id']))
        else:
            return r.json()['message']

    def query(self, query=None):
        query = query if query else Query(page_size=100)
        r = requests.post(self.database_query_api, headers=self.bot.headers, json=query.make())

        if r.status_code == 200:
            results = r.json()['results']
            while r.json()['has_more']:
                query = Query(page_size=100, start_cursor=r.json()['next_cursor'])
                r = requests.post(self.database_query_api, headers=self.bot.headers, json=query.make())
                results.extend(r.json()['results'])
            return results
        else:
            return r.json()['message']


    # async def async_post(self, data: PageObject, session):
    #     async with session.post(BaseObject.PageAPI, headers=self.bot.patch_headers, data=json.dumps(data.make())) as resp:
    #         if resp.status != 200:
    #             print(resp.status)
    #             print(await resp.text())
    #             print(data.template)
    #         return resp
    #         # try:
    #         #     return Page(bot=self.bot, page_id=str(resp.json()['id']))
    #         # except KeyError:
    #         #     print("Create failed")
    #         #     print(resp.json()['message'])
    #         #     return resp.json()['message']
    #

    # def query_database_page_list(self, query=None):
    #     results_list = self.query_database(query)
    #     results = [Page(self.bot, col['id'], parent=self) for col in results_list]
    #     return results
    #
    # def query_database_dataframe(self, query: Query = None):
    #     result_list = self.query_database(query)
    #     result = {p: [] for p in self.properties}
    #     for col in result_list:
    #         data = super().properties_data(col['properties'])
    #         for t, v in data.items():
    #             result[t].append(v)
    #     return result
    #
    #
    # def clear(self):
    #     delete_list = self.query_database_page_list()
    #     a = input(f"clear database id: {self.object_id} Y/N")
    #     if a == "y" or a == "Y":
    #         for database_page in delete_list:
    #             database_page.delete_object()
    #
    # async def async_clear(self, session):
    #     pages = []
    #     query = Query(page_size=100)
    #     q = query.make()
    #     async with session.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q)) as r:
    #         json_result = await r.json()
    #         pages.append(json_result["results"])
    #         start_course = json_result["next_cursor"]
    #
    #     if start_course and query.page_size == 100:
    #         while start_course:
    #             query.start_cursor = start_course
    #             query.page_size = 100
    #             q = query.make()
    #             async with session.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q)) as r:
    #                 json_result = await r.json()
    #                 pages.append(json_result["results"])
    #                 start_course = json_result["next_cursor"]
    #     pages_list = []  # list of page
    #     for p in pages:
    #         for col in p:
    #             pages_list.append(col)
    #
    #     pages_list = [Page(self.bot, col['id'], parent=self) for col in pages_list]
    #
    #     # a = input(f"clear database id: {self.object_id} Y/N")
    #     # if a == "y" or a == "Y":
    #     tasks = [database_page.async_delete_object(session) for database_page in pages_list]
    #     return await asyncio.gather(*tasks)
    #
    #
    #
