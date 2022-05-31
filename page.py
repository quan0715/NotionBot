import requests
from PyNotion import *


class Page:
    url = 'https://api.notion.com/v1/pages/'

    def __init__(self, Bot, page_id):
        self.Bot = Bot
        self.workspace = False
        self.page_id = page_id
        self.page_url = Page.url + self.page_id
        self.patch_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        self.parent_json = {
            "parent": {
                "type": "page_id",
                "page_id": self.page_id
            }
        }
        self.result = self.retrieve_page()
        self.parent = self.parent_init()

    def retrieve_page(self):
        #print(self.page_url)
        r = requests.get(self.page_url,headers=self.Bot.headers)
        return r.json()
    def parent_init(self):
        if self.result['parent']['type'] == 'workspace':
            self.workspace = True
        if self.result['parent']['type'] == 'database_id':
            return database.Database(database_id=self.result['parent']['database_id'], Bot=self.Bot)
        if self.result['parent']['type'] == 'page_id':
            return Page(page_id=self.result['parent']['page_id'],Bot=self.Bot)
        else:
            return None

    def append_block(self,children_array=None):
        children_template = {"children": children_array}
        r = requests.patch(self.patch_url, headers=self.Bot.patch_headers, data=json.dumps(children_template))
        return r.json()

    def update_page(self,data=None):
        data = {'object': 'page',
                'id': self.page_id,
                'parent': {'type': 'database_id', 'database_id': f"{self.parent.database_id}"},
                'icon': {'type': 'emoji', 'emoji': "🐶"}
        }
        r = requests.patch(self.page_url, headers=self.Bot.patch_headers, data=data)
        return r.json()
