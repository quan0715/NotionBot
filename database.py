import time
from PyNotion import *
from PyNotion.object import RichTextObject
from PyNotion.page import Page

class Database:
    def __init__(self, Bot, parent,database_id=None):
        self.init_url = "https://api.notion.com/v1/databases/"
        self.Bot = Bot
        self.parent = parent
        self.database_id = database_id
        self.database_url = f'https://api.notion.com/v1/databases/{database_id}'
        self.database_query_url = f'https://api.notion.com/v1/databases/{database_id}/query'
        self.properties = self.get_properties()
        self.results = self.query_database()

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

    def query_database(self, data=None):
        if data is None:
            r = requests.post(self.database_query_url,headers=self.Bot.headers)
        else:
            r = requests.post(self.database_query_url, headers=self.Bot.patch_headers, data=json.dumps(data))
        return r.json()['results']

    # def update_database(self, block_id, data):
    #     url = self.page.url + block_id
    #     requests.patch(url, headers=self.page.patch_headers,data=json.dumps(data))

    def create_post(self, row):
        try:
            r = requests.post(self.parent.url, headers=self.Bot.patch_headers, data=json.dumps(row))
            print(r.json())
            page_id = r.json()['id']
            return Page(Bot=self.Bot, page_id=page_id)
        except:
            return False

    def make_post(self, data):
        # def annotations(bold=False, italic=False, strikethrough=False, underline=False, code=False, color='default'):
        #     return {'bold': bold, 'italic': italic, 'strikethrough': strikethrough, 'underline': underline,
        #             "code": code, 'color': color}
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
                    'title' : t.object_array
                    # 'title': [{
                    #     'type': 'text',
                    #     'text': {'content': data[prop], 'link': None},
                    #     'annotations': annotations(),
                    #     'href': None}]
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
                    # 'rich_text': [{
                    #     'type': 'text',
                    #     'text': {'content': data[prop], 'link': None},
                    #     'annotations': annotations(),
                    #     'href': None}]
                }
            if self.properties[prop]['type'] == 'url':
                text['properties'][prop] = {
                    'type': 'url', "url": data[prop],
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
