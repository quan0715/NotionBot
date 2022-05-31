import time

from PyNotion import *
from PyNotion.object import RichTextObject
from PyNotion.base import Page


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
        # print(self.results)
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
        # print(r.json())
        return r.json()

    def query_database(self, data=None):

        result = {}
        if data is None:
            r = requests.post(self.database_query_url, headers=self.Bot.headers,data=json.dumps(query))
        else:
            r = requests.post(self.database_query_url, headers=self.Bot.patch_headers, data=json.dumps(data))
        result = r.json()['results']
        l = r.json()['results']
        while len(l[l.keys()[0]]) == 100:
            # max page size
            start_course += 100
            print(start_course)
            #r = requests.post(self.database_query_url, headers=self.Bot.headers,data=json.dumps(query))
            #f
        return r.json()['results']

    # def update_database(self, block_id, data):
    #     url = self.page.url + block_id
    #     requests.patch(url, headers=self.page.patch_headers,data=json.dumps(data))

    def create_post(self, row):
        # try:
        r = requests.post(self.parent_url, headers=self.Bot.patch_headers, data=json.dumps(row))
        print("good")
        page_id = r.json()['id']
        print(page_id)
        time.sleep(1)
        return Page(Bot=self.Bot, page_id=str(page_id))

    # except:
    #     print("wrong")
    #     return False

    def make_post(self, data):
        text = {
            'parent': {'type': 'database_id', 'database_id': f"{self.database_id}"},
            'archived': False,
            'properties': {

            }
        }
        for prop in data.keys():
            if self.properties[prop]['type'] == 'title':
                t = RichTextObject(plain_text=data[prop])
                text['properties'][prop] = {
                    'title': t.object_array
                }
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
            if self.properties[prop]['type'] == 'rich_text':
                t = RichTextObject(plain_text=data[prop])
                text['properties'][prop] = {
                    'rich_text': t.object_array
                }
            if self.properties[prop]['type'] == 'url':
                text['properties'][prop] = {
                    'type': 'url', "url": data[prop],
                }
            if self.properties[prop]['type'] == 'date':
                text['properties'][prop] = {
                    'type': 'date', 'date': data[prop]
                    # .update({"time_zone": "Etc/GMT+8"})
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
