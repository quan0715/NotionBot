from PyNotion import *
from PyNotion.database import *
from PyNotion.page import *
from typing import Union
from PyNotion.object import *


class Notion:
    user_api = "https://api.notion.com/v1/users/me"
    api = f'https://api.notion.com/v1'
    search_api = 'https://api.notion.com/v1/search'
    notion_version = "2022-06-28"
    search_database_api = 'https://api.notion.com/v1/databases'

    def __init__(self, auth: str):
        """
        :param auth: your notion integration internal token
        """
        self.auth = auth
        self.headers = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.notion_version,
            "Accept": "application/json",
        }
        self.patch_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.notion_version,
            'Content-Type': 'application/json'
        }
        self.bot = self.bot_user()

    def bot_user(self):
        api = "https://api.notion.com/v1/users/me"
        r = requests.get(api, headers=self.headers)
        if r.status_code == 200:
            print(f"Connect to integration {r.json()['name']}")
            return r.json()
        else:
            print("Connect failed please request again !!!")
            return None

    def retrieve(self, url):
        r = requests.get(url, headers=self.headers)
        return r.json()

    def fetch_databases(self, title):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'database', 'property': 'object'},
            'page_size': 100
        }
        response = requests.request("POST", self.search_api, json=payload, headers=self.patch_headers)
        if response.json()['results']:
            # print(response.text)
            text = response.json()['results'][0]
            database_id = text['id']
            # page_id = text['parent']['page_id']
            # print(page_id)
            # page = page(page_id=page_id,Bot=self)
            return Database(bot=self, database_id=database_id)
        else:
            print(f"Can't find DataBase {title}")
            return None

    def fetch_page(self, title):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'page', 'property': 'object'},
            'page_size': 100
        }
        response = requests.post(self.search_api, json=payload, headers=self.patch_headers)
        # print(response.json())
        if response.status_code == 200:
            # print(response.text)
            text = response.json()['results'][0]
            page_id = text['id']
            # print(page_id)
            print(f"fetch {title} page successfully")
            return Page(page_id=page_id, bot=self)
        else:
            print(f"Can't find page {title}")

        return None


    @staticmethod
    def create_new_page(parent: Union[Page, Database], data):
        if isinstance(parent, Database):
            return parent.post(parent.new_page(data))

        elif isinstance(parent, Page):
            return parent.create_page(data)

    def append_block(self, target_page: Page, children_array):
        target_page.append_children(children_array)

    def update_page(self,target, data):
        if isinstance(target.parent, Database):
            data = target.parent.post_template(data)
        target.update(data)


    def create_new_database(self, parent: Page, title=None, properties=None, icon=None, cover=None, is_inline=False):
        r = parent.create_database(title=title, properties=properties,icon=icon,cover=cover,is_inline=is_inline)
        if r.status_code == 200:
            print(f"create_new_database successfully id {r.json()['id']} ")
            return Database(self, r.json()['id'])
        else:
            print(r.json()['message'])
