from PyNotion import *
import requests


class Page:
    def __init__(self, Bot, page_id):
        self.Bot = Bot
        self.page_id = page_id
        self.url = f'https://api.notion.com/v1/pages/'
        self.search_url = "https://api.notion.com/v1/search"
        self.patch_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        self.parent_json = {
            "parent": {
                "type": "page_id",
                "page_id": self.page_id
            }
        }

    # def create_database(self):

    def get_database_id(self, target):
        r = requests.post(self.search_url, headers=self.Bot.patch_headers)
        print(target)
        j = json.loads(r.text)
        results = j['results']
        for r in results:
            if r['object'] == 'database' and r['title'][0]['text']['content'] == target:
                return r['id']
        return False

    def append_block(self,children_array=None):
        template = {"children":children_array}
        r = requests.patch(self.patch_url, headers=self.Bot.patch_headers, data=json.dumps(template))
        print(r.json())
