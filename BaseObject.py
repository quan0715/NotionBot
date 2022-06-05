from PyNotion import *
from PyNotion.Object import *


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
        if isinstance(data, list):
            data = ChildrenObject(*data)
        if isinstance(data, ChildrenObject):
            data = data.get_template()
        if isinstance(data, dict):
            data = json.dumps(data)
        elif not isinstance(data, str):
            print("Wrong input format")
            #data = json.dumps(data.get_template())
        print(data)
        url = BaseObject.BlockAPI + self.object_id + "/children"
        r = requests.patch(url, headers=self.bot.patch_headers, data=data)
        if r.status_code != 200:
            return r.json()['message']
        else:
            #result_list = [dict(block_id = result['id'],type= result['type'],has_children = result['has_children']) for result in r.json()['results']]
            return r.json()['results']

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
    def __init__(self, bot, page_id, parent=None):
        super().__init__(bot, page_id)
        self.page_url = BaseObject.PageAPI + self.object_id
        self.page_property = self.page_url + "/properties/"
        self.patch_url = f"https://api.notion.com/v1/blocks/{self.object_id}/children"
        self.parent_root = ParentObject(parent_type=ParentType.page, parent_id=self.object_id)
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
        return self.update(EmojiObject(emoji).get_json(), )

    def create_page(self, data):
        r = requests.post(Page.PageAPI, headers=self.bot.patch_headers, data=json.dumps(data))
        try:
            return Page(bot=self.bot, page_id=str(r.json()['id']))
        except KeyError:
            print("create failed")
            return r.json()

    def create_database(self, title, properties=None):
        template = dict(
            parent=self.parent_root.template,
            title=TextObject(content=title).template
        )
        if isinstance(properties, PropertyObject):
            template.update(dict(properties=properties.get_template()))
        else:
            properties = PropertyObject({"UnTitle": TitleProperty()})
            template.update(dict(properties=properties.get_template()))

        r = requests.post(BaseObject.DatabaseAPI, headers=self.bot.patch_headers, data=json.dumps(template))
        if r.status_code == 200:
            print(f"database {title} 創建成功,你可以在 page_id {self.object_id} 找到他")
            return r.json()
        else:
            print(r.json()['message'])

class Database(BaseObject):
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

    def database_detail(self):
        r = self.retrieve()
        result_dict = r['properties']
        result = {key: {"type": result_dict[key]['type'], "id": result_dict[key]['id']} for key in result_dict.keys()}
        parent_type = r['parent']['type']
        parent_id = r['parent'][parent_type]
        return r, result, ParentObject(parent_type, parent_id)

    def query_database(self, query=None):
        pages = []
        query = query if query else Query(page_size=100)
        q = query.make_template()
        r = requests.post(self.database_query_url, headers=self.bot.patch_headers, data=json.dumps(q))
        pages.append(r.json()["results"])
        start_course = r.json()["next_cursor"]
        if start_course and query.page_size == 100:
            while start_course:
                query.start_cursor = start_course
                query.page_size = 100
                q = query.make_template()
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
                prop_dict[prop] = {'type': 'date', 'date': value}

        return {
            'parent': ParentObject(ParentType.database, self.object_id).template,
            'archived': False,
            'properties': prop_dict
        }


class Block(BaseObject):
    def __init__(self, bot, block_id):
        super().__init__(bot, block_id)
        self.block_url = BaseObject.BlockAPI + self.object_id
        self.children_url = f'{self.block_url}/children'

    def retrieve(self, **kwargs):
        return super().retrieve(self.block_url)

    def update(self, data, **kwargs):
        return super().update(self.block_url, data)


