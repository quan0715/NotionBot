from PyNotion import *
from PyNotion.database import *
from PyNotion.page import *
from PyNotion.block import *
from typing import Union
from PyNotion.object import *
from dotenv import load_dotenv
import os


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

    @classmethod
    def retrieve_from(cls, target: Union[Page, Database, Block]):
        return target.retrieve()

    @staticmethod
    def create_new_page(parent: Union[Page, Database], content: PageObject):
        if isinstance(parent, Database):
            return parent.post(parent.new_page(content))

        elif isinstance(parent, Page):
            return parent.create_page(content)

    def fetch_databases(self, title: str):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'database', 'property': 'object'},
            'page_size': 100
        }
        response = requests.request("POST", self.search_api, json=payload, headers=self.patch_headers)
        if response.json()['results']:
            text = response.json()['results'][0]
            database_id = text['id']
            print(f"fetching database {title} successfully")
            return Database(bot=self, database_id=database_id)

        else:
            print(f"Can't find database {title}, check if it exist in your notion page")

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

    def append_block(self, target_page: Page, children_array):
        target_page.append_children(children_array)

    def update_page(self, target, data):
        if isinstance(target.parent, Database):
            data = target.parent.new_page(data)
        target.update(data)

    def create_new_database(self, parent: Page, title=None, properties=None, icon=None, cover=None, is_inline=False):
        r = parent.create_database(title=title, properties=properties, icon=icon, cover=cover, is_inline=is_inline)
        if r.status_code == 200:
            print(f"create_new_database successfully id {r.json()['id']} ")
            return Database(self, r.json()['id'])
        else:
            print(r.json()['message'])


class Async_Notion_Bot:
    user_api = "https://api.notion.com/v1/users/me"
    api = f'https://api.notion.com/v1'
    search_api = 'https://api.notion.com/v1/search'
    notion_version = "2022-06-28"
    search_database_api = 'https://api.notion.com/v1/databases'

    def __init__(self, auth: str, session):
        """
        :param auth: your notion integration internal token
        """
        self.auth = auth
        self.session = session
        self.headers = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.NOTION_VERSION,
            "Accept": "application/json",
        }
        self.patch_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.NOTION_VERSION,
            'Content-Type': 'application/json'
        }
        self.bot = self.bot_user()

    async def bot_user(self):
        r = await self.session.get(self.USER_API, headers=self.headers)
        if r.status_code == 200:
            json_resp = await r.json()
            print(f"Connect to integration {json_resp['name']}")
            return json_resp
        else:
            print("Connect failed please request again !!!")
            return None

    def retrieve(self, url):
        r = requests.get(url, headers=self.headers)
        return r.json()

    async def search(self, title: str,
                     sort: SearchSort = SearchSort(),
                     target: Union[BaseObject.Type, str] = BaseObject.Type.page,
                     limit: int = 100):
        payload = dict(
            query=title,
            filter=dict(value=target, property="object"),
            page_size=limit,
        )
        payload.update(sort.make())
        async with self.session.post(self.SEARCH_API, json=payload, headers=self.patch_headers) as resp:
            json_resp = await resp.json()
            if json_resp['results']:
                text = json_resp['results'][0]
                index = text['id']
                print(f"fetching {target} {title} successfully")
                if target == BaseObject.Type.page:
                    return Page(bot=self, page_id=index)
                else:
                    return Database(bot=self, database_id=index)
            else:
                print(f"Can't find {target} {title}, check if it exist in your notion page")
                return None

    async def fetch_databases(self, title: str, sort: SearchSort = SearchSort(), limit=1) -> Database:
        return await self.search(title, sort=sort, target=BaseObject.Type.database, limit=limit)

    async def fetch_pages(self, title: str, sort: SearchSort = SearchSort(), limit=1) -> Page:
        return await self.search(title, sort=sort, target=BaseObject.Type.page, limit=limit)

    @staticmethod
    def create_new_page(parent: Union[Page, Database], data):
        if isinstance(parent, Database):
            return parent.post(parent.new_page(data))

        elif isinstance(parent, Page):
            return parent.create_page(data)

    async def append(self, target_page: Page, children_array):
        pass

    async def update(self, target, data):
        pass

    async def create_database(self, parent: Page, title=None, properties=None, icon=None, cover=None, is_inline=False):
        pass

    async def create_page(self):
        pass
