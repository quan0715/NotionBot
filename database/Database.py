from PyNotion import *
from PyNotion.page.Page import Page
from PyNotion.object import *
import asyncio
import aiohttp

class Database(BaseObject):
    API = "https://api.notion.com/v1/databases/"

    def __init__(self, bot, database_id: str):
        super().__init__(bot, database_id)
        self.database_url = BaseObject.DatabaseAPI + database_id
        self.database_query_url = f'{self.database_url}/query'
        self.result_list = self.query_database()
        self.database_detail, self.properties, self.parent = self.database_detail()

    def retrieve(self, **kwargs):
        return super().retrieve(self.database_url)

    def update(self, data, **kwargs):
        return super().update(self.database_url, data)

    async def async_post(self, data, session):
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

    def post(self, data):
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

    def new_page(self, *post_list):
        return DatabasePage(self, *post_list)


    # def post_template(self, data: dict[str:str]) -> dict:
    #     prop_dict = {}
    #     for prop, value in data.items():
    #         value_type = self.properties[prop]['type']
    #         if value_type == Text.Type.title or value_type == Text.Type.rich_text:
    #             prop_dict[prop] = {f'{value_type}': Text(content=str(value)).make()}
    #         if value_type == Number.Type.number:
    #             if type(value) == str:
    #                 if value == '':
    #                     value = "-1"
    #                 if value.endswith('%'):
    #                     value = value.split('%')[0]
    #                 value = eval(value)
    #             prop_dict[prop] = {'type': value_type, value_type: value}
    #
    #         if value_type == Option.Type.select:
    #             prop_dict[prop] = {'type': 'select', 'select': {'name': value}}
    #
    #         if value_type == 'url':
    #             prop_dict[prop] = Link(value).template
    #
    #         if value_type == 'date':
    #             prop_dict[prop] = {'type': 'date', 'date': value}
    #
    #     return {
    #         'parent': Parent(Parent.Type.database, self.object_id).make(),
    #         'archived': False,
    #         'properties': prop_dict
    #     }


class DatabasePage:
    def __init__(self, target: Database, *post_list):
        self.template = {
            'parent': Parent(Parent.Type.database, target.object_id).make(),
            'archived': False,
            'properties': {}
        }
        for p in post_list:
            self.template['properties'].update(p.make())

    def make(self):
        return self.template

