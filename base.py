import time
from PyNotion import *
from PyNotion.object import RichTextObject


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
        #print(self.page_url)
        r = requests.get(self.page_url,headers=self.Bot.headers)
        print(r.json())
        return r.json()

    def parent_init(self):
        if self.result['parent']['type'] == 'workspace':
            self.workspace = True
        if self.result['parent']['type'] == 'database_id':
            return Database(database_id=self.result['parent']['database_id'], Bot=self.Bot)
        if self.result['parent']['type'] == 'page_id':
            return Page(page_id=self.result['parent']['page_id'],Bot=self.Bot)
        else:
            return None


    def append_block(self,children_array=None):
        children_template = {"children": children_array}
        r = requests.patch(self.patch_url, headers=self.Bot.patch_headers, data=json.dumps(children_template))
        return r.json()

    def update_page(self,data):
        r = requests.patch(self.page_url, headers=self.Bot.patch_headers, data=json.dumps(data))

        return r.json()


    @classmethod
    def create_page(cls, Bot, data):
        r = requests.post(Page.url, headers=Bot.patch_headers, data=json.dumps(data))
        page_id = r.json()['id']
        return Page(Bot=Bot, page_id=str(page_id))

class Database:
    url = "https://api.notion.com/v1/databases/"

    def __init__(self, Bot, database_id):
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
        result_dict = r.json()
        return result_dict['properties']

    def retrieve_database(self):
        r = requests.get(self.database_url, headers=self.Bot.headers)
        return r.json()

    def query_database(self, data=None):
        if data is None:
            r = requests.post(self.database_query_url, headers=self.Bot.headers)
        else:
            r = requests.post(self.database_query_url, headers=self.Bot.patch_headers, data=json.dumps(data))
        return r.json()['results']

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
            if self.properties[prop]['type'] in ['title','rich_text']:
                text['properties'][prop] = {f'{self.properties[prop]["type"]}': RichTextObject(plain_text=data[prop]).object_array}
            if self.properties[prop]['type'] == 'number':
                n = data[prop]
                if type(n) == str:
                    if n == '':
                        n = "-1"
                    if n.endswith('%'):
                        n = n.split('%')[0]
                    n = eval(n)
                text['properties'][prop] = {'type': 'number', 'number': n}

            if self.properties[prop]['type'] == 'select':
                text['properties'][prop] = {
                    'type': 'select',
                    'select': {'name': data[prop]}
                }

            if self.properties[prop]['type'] == 'url':
                text['properties'][prop] = {
                    'type': 'url', "url": data[prop],
                }

            if self.properties[prop]['type'] == 'date':
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
