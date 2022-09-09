from PyNotion import *
from PyNotion.page.Page import Page, PageObject
from PyNotion.object import *
import asyncio
import aiohttp
from typing import Union


class Database(BaseObject):
    API = "https://api.notion.com/v1/databases/"
    object = "database"

    def __init__(self, bot, database_id: str):
        super().__init__(bot, database_id)
        self.database_url = BaseObject.DatabaseAPI + database_id
        self.database_query_url = f'{self.database_url}/query'
        self.result_list = self.query_database()
        self.details: dict = self.retrieve()
        self.created_by = self.details['created_by']
        self.last_edited_by = self.details['last_edited_by']
        self.last_edited_time = self.details['last_edited_time']
        self.title = self.details['title'][0]['text']['content']
        self.is_inline = self.details['is_inline']
        self.archived = self.details['archived']
        self.parent = self.get_parent()
        self.properties = self.details['properties']
        # self.properties =
        # self.database_detail, self.properties, self.parent = self.database_detail()

    def __repr__(self):
        return f"""------------------------------------------------------
{self.parent}
------------------------------------------------------
Object : {self.object} 
title : {self.title}
id : {self.object_id}
------------------------------------------------------
created_by : {self.created_by}
last_edited_by : {self.last_edited_by}
last_edited_time : {self.last_edited_time}
------------------------------------------------------
is_inline : {self.is_inline}
archive : {self.archived}
url : {self.database_url}
------------------------------------------------------
Property : 
{self.print_properties()}
------------------------------------------------------
"""

    def retrieve(self, **kwargs) -> dict:
        return super().retrieve(self.database_url)

    def update(self, data, **kwargs):
        return super().update(self.database_url, data)

    def print_properties(self):
        r = [f"\t{v['name']} --- {v['type']} --- {v['id']}" for v in self.properties.values()]
        return "\n".join(r)

    def get_parent(self):
        return Parent(
            parent_type=self.details['parent']['type'],
            parent_id=self.details['parent'][self.details['parent']['type']]
        )

    async def async_post(self, data: PageObject, session):
        async with session.post(BaseObject.PageAPI, headers=self.bot.patch_headers, data=json.dumps(data.make())) as resp:
            print(resp.status)
            print(await resp.text())
            return resp
            # try:
            #     return Page(bot=self.bot, page_id=str(resp.json()['id']))
            # except KeyError:
            #     print("Create failed")
            #     print(resp.json()['message'])
            #     return resp.json()['message']

    def post(self, data: PageObject):
        r = requests.post(BaseObject.PageAPI, headers=self.bot.patch_headers, data=json.dumps(data.make()))
        try:
            return Page(bot=self.bot, page_id=str(r.json()['id']))
        except KeyError:
            print("Create failed")
            print(r.json()['message'])
            return r.json()['message']

    def get_properties(self):
        # get database properties
        r = requests.get(self.database_url, headers=self.bot.patch_headers)
        result_dict = r.json()['properties']
        result = {key: {"type": result_dict[key]['type'], "id": result_dict[key]['id']} for key in result_dict.keys()}
        return result

    def database_detail(self):
        r = self.retrieve()
        result_dict = r['properties']
        result = {key: {"type": result_dict[key]['type'], "id": result_dict[key]['id']} for key in result_dict.keys()}
        parent_type = r['parent']['type']
        parent_id = r['parent'][parent_type]
        return r, result, Parent(parent_type, parent_id)

    def query_database(self, query=None):
        pages = []
        query = query if query else Query(page_size=100)
        q = query.make()
        r = requests.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q))
        pages.append(r.json()["results"])
        start_course = r.json()["next_cursor"]
        if start_course and query.page_size == 100:
            while start_course:
                query.start_cursor = start_course
                query.page_size = 100
                q = query.make()
                r = requests.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q))
                pages.append(r.json()["results"])
                start_course = r.json()["next_cursor"]
        pages_list = []  # list of page
        for p in pages:
            for col in p:
                pages_list.append(col)
        return pages_list

    def query_database_page_list(self, query=None):
        results_list = self.query_database(query)
        results = [Page(self.bot, col['id'], parent=self) for col in results_list]
        return results

    def query_database_dataframe(self, query: Query = None):
        result_list = self.query_database(query)
        result = {p: [] for p in self.properties}
        for col in result_list:
            data = super().properties_data(col['properties'])
            for t, v in data.items():
                result[t].append(v)
        return result

    def new_page(self, prop_value, children=None, icon=None, cover=None) -> PageObject:
        return PageObject(
            parent=Parent(Parent.Type.database, self.object_id),
            prop_value=prop_value,
            children=children,
            icon=icon,
            cover=cover
        )

    def clear(self):
        delete_list = self.query_database_page_list()
        a = input(f"clear database id: {self.object_id} Y/N")
        if a == "y" or a == "Y":
            for database_page in delete_list:
                database_page.delete_object()

    async def async_clear(self, session):
        pages = []
        query = Query(page_size=100)
        q = query.make()
        async with session.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q)) as r:
            json_result = await r.json()
            pages.append(json_result["results"])
            start_course = json_result["next_cursor"]

        if start_course and query.page_size == 100:
            while start_course:
                query.start_cursor = start_course
                query.page_size = 100
                q = query.make()
                async with session.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q)) as r:
                    json_result = await r.json()
                    pages.append(json_result["results"])
                    start_course = json_result["next_cursor"]
        pages_list = []  # list of page
        for p in pages:
            for col in p:
                pages_list.append(col)

        pages_list = [Page(self.bot, col['id'], parent=self) for col in pages_list]

        # a = input(f"clear database id: {self.object_id} Y/N")
        # if a == "y" or a == "Y":
        tasks = [database_page.async_delete_object(session) for database_page in pages_list]
        return await asyncio.gather(*tasks)



