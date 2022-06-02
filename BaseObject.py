from PyNotion import *
from PyNotion.Object import *
from abc import ABC, abstractmethod


# from PyNotion.NotionClient import Notion


class BaseObject:
    def __init__(self, bot, object_id):
        self.bot = bot
        self.object_id = object_id

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
                else:
                    result[key] = "None"
            except:
                result[key] = "None"
        return result


class Page(BaseObject):
    PageAPI = 'https://api.notion.com/v1/pages/'
    def __init__(self, bot, page_id, parent=None):
        super().__init__(bot, page_id)
        self.page_url = Page.PageAPI + self.object_id
        self.page_property = self.page_url + "/properties/"
        self.patch_url = f"https://api.notion.com/v1/blocks/{self.object_id}/children"
        self.parent = parent

    def retrieve_property_item(self,property_id):
        r = requests.get(url=self.page_property+property_id, headers=self.bot.headers)
        return r.json()

    def retrieve(self):
        return self.bot.retrieve(self.page_url)

    def retrieve_page_data(self):
        # database only
        if not isinstance(self.parent, Database):
            print("can't change to dataframe")
            return False
        r = self.retrieve()
        properties = r['properties']
        result = super().properties_data(properties)
        return result

    def append_block(self, children_array=None):
        children_template = {"children": children_array}
        r = requests.patch(self.patch_url, headers=self.bot.patch_headers, data=json.dumps(children_template))
        return r.json()

    def update(self, data):
        data = data if isinstance(data, str) else json.dumps(data)
        r = requests.patch(self.page_url, headers=self.bot.patch_headers, data=json.dumps(data))
        return r.json()

    def update_emoji(self, emoji: str):
        return self.update(EmojiObject(emoji).get_json())

    @classmethod
    def create_page(cls, bot, data):
        r = requests.post(cls.PageAPI, headers=bot.patch_headers, data=json.dumps(data))
        try:
            return Page(bot=bot, page_id=str(r.json()['id']))
        except KeyError:
            print("create faild")
            return r.json()


class Database(BaseObject):
    database_api = "https://api.notion.com/v1/databases/"
    def __init__(self, bot, database_id: str):
        super().__init__(bot,database_id)
        self.database_url = Database.database_api + database_id
        self.database_query_url = f'{self.database_url}/query'
        self.result_list = self.query_database()
        self.database_detail, self.properties, self.parent = self.retrieve_database()


    def post(self, data):
        data = data if isinstance(data,str) else json.dumps(data)
        r = requests.post(Page.PageAPI, headers=self.bot.patch_headers, data=data)
        try:
            return Page(bot=self.bot, page_id=str(r.json()['id']))
        except KeyError:
            print("Create failed")
            return r.json()

    def get_properties(self):
        # get database properties
        r = requests.get(self.database_url, headers=self.bot.patch_headers)
        result_dict = r.json()['properties']
        result = {key: {"type": result_dict[key]['type'], "id": result_dict[key]['id']} for key in result_dict.keys()}
        return result

    def retrieve_database(self):
        r = requests.get(self.database_url, headers=self.bot.headers)
        result_dict = r.json()['properties']
        result = {key: {"type": result_dict[key]['type'], "id": result_dict[key]['id']} for key in result_dict.keys()}
        parent_type = r.json()['parent']['type']
        parent_id = r.json()['parent'][parent_type]
        return r.json(), result, ParentObject(parent_type, parent_id)

    def query_database(self, query=None):
        pages = []
        q = query.template if query else {"page_size": 100}
        r = requests.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q))
        pages.append(r.json()["results"])
        start_course = r.json()["next_cursor"]
        if start_course and query.page_size == 100:
            while start_course:
                query.start_cursor = start_course
                query.page_size = 100
                q = query.make_template()
                r = requests.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q))
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

    def post_template(self, data: dict[str:str]) -> dict:
        prop_dict = {}
        for prop, value in data.items():
            value_type = self.properties[prop]['type']
            if value_type == Text.Type.title or value_type == Text.Type.rich_text:
                t = TextObject(content=value).template
                prop_dict[prop] = {f'{value_type}': t}
            if value_type == Number.Type.number:
                if type(value) == str:
                    if value == '':
                        value = "-1"
                    if value.endswith('%'):
                        value = value.split('%')[0]
                    value = eval(value)
                prop_dict[prop] = {'type': value_type, value_type: value}

            if value_type == Select.Type.select:
                prop_dict[prop] = {'type': 'select', 'select': {'name': value}}

            if value_type == 'url':
                prop_dict[prop] = LinkObject(value).template

            if value_type == 'date':
                prop_dict[prop]['type'] = {'type': 'date', 'date': value}

        return {
            'parent': ParentObject(ParentType.database, self.object_id).template,
            'archived': False,
            'properties': prop_dict
        }
