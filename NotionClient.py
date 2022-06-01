from PyNotion import *
from PyNotion import Database, Page
from PyNotion.Object import *


class Notion:

    def __init__(self, auth):
        self.auth = auth
        self.url = f'https://api.notion.com/v1'
        self.search_url = self.url + "/search"
        self.search_database = self.url + "/databases?page_size=100"
        self.notion_version = "2022-02-22"
        self.headers = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.notion_version,
            "Accept": "application/json",
        }
        self.patch_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.notion_version,

        }

    def retrieve(self, url):
        r = requests.get(url, headers=self.headers)
        return r.json()

    def fetch_databases(self, title):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'database', 'property': 'object'},
            'page_size': 100
        }
        response = requests.request("POST", self.search_url, json=payload, headers=self.patch_headers)
        # print(response.json())
        if response.json()['results']:
            # print(response.text)
            text = response.json()['results'][0]
            database_id = text['id']
            # page_id = text['parent']['page_id']
            # print(page_id)
            # page = Page(page_id=page_id,Bot=self)
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
        response = requests.post(self.search_url, json=payload, headers=self.patch_headers)
        # print(response.json())
        if response.json()['results']:
            # print(response.text)
            text = response.json()['results'][0]
            page_id = text['id']
            # print(page_id)
            return Page(page_id=page_id, bot=self)
        else:
            print(f"Can't find Page {title}")

        return None

    def create_new_page(self, data, database=None):
        if database:
            p = database.post(self, database.make_post(data))
        else:
            p = Page.create_page(self, data)
        return p

    def append_block(self, target_page, children_array):
        pass

    def update_page(self,target, data):
        if isinstance(target.parent, Database):
            data = target.parent.post_template(data)
        target.update(data)

    def create_post_template(self, target, data):
        template = {
            'parent': ParentObject(target.type, target.id).template,
            'archived': False,
            'properties': {}
        }




