from PyNotion import *
from PyNotion.object import *


class Page:
    url = 'https://api.notion.com/v1/pages/'

    def __init__(self, Bot, page_id):
        self.Bot = Bot
        self.workspace = False
        self.page_id = page_id
        self.page_url = Page.url + self.page_id
        self.patch_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        # self.parent_json = {
        #     "parent": {
        #         "type": "page_id",
        #         "page_id": self.page_id
        #     }
        # }
        self.result = self.retrieve_page()
        self.parent = self.parent_init()

    def retrieve_page(self):
        # print(self.page_url)
        r = requests.get(self.page_url, headers=self.Bot.headers)
        #print(r.json())
        return r.json()

    def parent_init(self):
        if self.result['parent']['type'] == 'workspace':
            self.workspace = True
        if self.result['parent']['type'] == 'database_id':
            return Database(database_id=self.result['parent']['database_id'], Bot=self.Bot)
        if self.result['parent']['type'] == 'page_id':
            return Page(page_id=self.result['parent']['page_id'], Bot=self.Bot)
        else:
            return None

    def append_block(self, children_array=None):
        children_template = {"children": children_array}
        r = requests.patch(self.patch_url, headers=self.Bot.patch_headers, data=json.dumps(children_template))
        return r.json()

    def update_page(self, data):
        r = requests.patch(self.page_url, headers=self.Bot.patch_headers, data=json.dumps(data))
        return r.json()

    def update_emoji(self,emoji: str):
        return self.update_page(Emoji_object(emoji).get_json())

    @classmethod
    def create_page(cls, Bot, data):
        r = requests.post(Page.url, headers=Bot.patch_headers, data=json.dumps(data))
        try:
            page_id = r.json()['id']
            return Page(Bot=Bot, page_id=str(page_id))
        except KeyError:
            return r.json()


class Database:
    url = "https://api.notion.com/v1/databases/"

    def __init__(self, Bot, database_id:str):
        self.Bot = Bot
        self.database_id = database_id
        self.database_url = Database.url + database_id
        self.database_query_url = f'{self.database_url}/query'
        self.properties = self.get_properties()
        self.results = self.query_database()
        self.database_detail = self.retrieve_database()
        self.parent_id = self.database_detail['parent']['page_id']
        self.parent_url = "https://api.notion.com/v1/pages"

    # def create_new_database(self, title, properties):
    #     data = self.Bot.parent_json
    #     data['icon'] = None
    #     data['cover'] = None
    #     data["title"] = [
    #         {
    #             "type": "text",
    #             "text": {
    #                 "content": f"{title}",
    #                 "link": None
    #             }
    #         }
    #     ]
    #     data["properties"] = properties
    #     r = requests.post(
    #         self.init_url,
    #         headers=self.Bot.patch_headers,
    #         data=json.dumps(data)
    #     )
    #     time.sleep(2)
    #     database_id = self.page.get_database_id(target=title)
    #     print(database_id)
    #     if database_id:
    #         print(f"database 新增成功")
    #         self.id_init(database_id)
    #     else:
    #         print("Error")

    def get_properties(self):
        # get database properties
        r = requests.get(self.database_url, headers=self.Bot.patch_headers)
        result_dict = r.json()['properties']
        result = {key: result_dict[key]['type'] for key in result_dict.keys()}
        return result

    def retrieve_database(self):
        r = requests.get(self.database_url, headers=self.Bot.headers)
        return r.json()

    def query_database(self, data=None):
        start_course = ""
        page = []
        if data is None:
            r = requests.post(self.database_query_url, headers=self.Bot.headers)
        else:
            r = requests.post(self.database_query_url, headers=self.Bot.patch_headers, data=json.dumps(data))
        page.append(r.json()['results'])
        start_course = r.json()["next_cursor"]
        while start_course:
            #print(start_course)
            query = {
                "start_cursor": start_course,
                "page_size": 100
            }
            r = requests.post(self.database_query_url, headers=self.Bot.patch_headers, data=json.dumps(query))
            start_course = r.json()["next_cursor"]
            page.append(r.json()['results'])

        result_list = {k:[] for k in self.properties.keys()}
        result_list['page_id'] = []
        for p in page:
            for column in p:
                col = column['properties']
                result_list['page_id'].append(column['id'])
                #print(col)
                for key,value in col.items():
                    prop_type =self.properties[key]
                    if prop_type in ['title', 'rich_text']:
                        result_list[key].append(value[prop_type][0]['plain_text'])
                    if prop_type in ['number','url']:
                        result_list[key].append(value[prop_type])
                    if prop_type == 'select':
                        result_list[key].append(value[prop_type]['name'])
                    if prop_type == 'date':
                        text = value[prop_type]['start']
                        if value[prop_type]['end']:
                            text += f" ~ {value[prop_type]['end']}"
                        #if value[prop_type]['start']
                        result_list[key].append(text)
                    else:
                        result_list[key].append("None")
        return result_list

    # def update_database(self, block_id, data):
    #     url = self.page.url + block_id
    #     requests.patch(url, headers=self.page.patch_headers,data=json.dumps(data))

    def make_post(self, data):
        text = {
            'parent': {'type': 'database_id', 'database_id': f"{self.database_id}"},
            'archived': False,
            'properties': {

            }
        }
        for prop in data.keys():
            if self.properties[prop] in ['title', 'rich_text']:
                t = TextObject(content=data[prop]).object_array
                text['properties'][prop] = {f'{self.properties[prop]}': t}
            if self.properties[prop] == 'number':
                n = data[prop]
                if type(n) == str:
                    if n == '':
                        n = "-1"
                    if n.endswith('%'):
                        n = n.split('%')[0]
                    n = eval(n)
                text['properties'][prop] = {'type': 'number', 'number': n}

            if self.properties[prop] == 'select':
                text['properties'][prop] = {
                    'type': 'select',
                    'select': {'name': data[prop]}
                }

            if self.properties[prop] == 'url':
                text['properties'][prop] = LinkObject(data[prop]).template

            if self.properties[prop] == 'date':
                text['properties'][prop] = {
                    'type': 'date', 'date': data[prop]
                }

        return text

    def make_filter(self, filter=None, sort=None, page_size=None):
        """
        filter -> dict
        sort -> list
        """
        template = {
            "filter": {

            },
            "sorts": [

            ]
        }
        if filter:
            template['filter'][filter[0]] = []
            for f in filter[1]:
                filter_object = {
                    "property": f['property'],
                    f['type']: {
                        f['condition']: f['target']
                    }
                }
                template['filter'][filter[0]].append(filter_object)
        if sort:
            for s in sort:
                template['sorts'].append(
                    {
                        "property": s['property'],
                        "direction": "ascending" if s['direction'] else "descending"
                    }
                )
        if page_size:
            template['page_size'] = page_size
        return template
