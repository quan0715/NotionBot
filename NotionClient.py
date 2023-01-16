import requests
from bs4 import BeautifulSoup
import os
from page import *
from block import *
from object import *
from database import *

class Notion:
    user_api = "https://api.notion.com/v1/users/me"
    api = f'https://api.notion.com/v1'
    notion_version = "2022-06-28"
    search_database_api = 'https://api.notion.com/v1/databases'

    def __init__(self, auth: str):
        """
        :param auth: your notion integration internal token
        """
        self.auth = auth
        self.headers = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": Notion.notion_version,
            "Accept": "application/json",

        }
        self.patch_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth}",

        }
        # self.bot = self.bot_user()

    def get_user(self):
        api = "https://api.notion.com/v1/users/me"
        r = requests.get(api, headers=self.headers)
        if r.status_code == 200:
            print(f"Connect to integration {r.json()['name']}")
            return r.json()
        else:
            print("Connect failed please request again !!!")
            return None

    def search(self, target=None):
        payload = {
            'query': f'{target}',
            'page_size': 100
        }
        search_api = 'https://api.notion.com/v1/search'
        r = requests.post(search_api, headers=self.headers, json=payload)
        if r.status_code == 200:
            return r.json()
        else:
            # print("Connect failed please request again !!!")
            return None

    def get_block(self, block_id) -> Block:
        api = f"https://api.notion.com/v1/blocks/{block_id}"
        r = requests.get(api, headers=self.headers)
        if r.status_code == 200:
            return Block(self, block_id)
        else:
            return r.json()

    def get_page(self, page_id) -> Page:
        api = f"https://api.notion.com/v1/pages/{page_id}"
        r = requests.get(api, headers=self.headers)
        if r.status_code == 200:
            # print(f"Connect to integration {r.json()['name']}")
            return Page(self, page_id)
        else:
            return r.json()
            # print("Connect failed please request again !!!")

    def get_database(self, database_id):
        database_api = f'https://api.notion.com/v1/databases/{database_id}'
        r = requests.get(database_api, headers=self.headers)
        if r.status_code == 200:
            return Database(self, r.json()['id'])
        else:
            print("Connect failed please request again !!!")
            return None


    def create_new_page(self,
                        parent: Union[Page, Parent],
                        properties: Union[Properties, dict] = Properties(),
                        children: Union[Children, dict] = Children(),
                        icon: Union[Emoji, str] = Emoji('🐧'),
                        cover: Union[File, str] = None):
        """
        :param parent: the database parent or page parent. please use Parent object or json format
        :param properties: Properties value of this page. please use Properties object or json format
        :param children: Page content for the new page as an array of block objects. please use Children object or json format
        :param icon: Page icon for the new page. Please use Emoji Object or string emoji.
        :param cover: Page cover for the new page. Please use File Object.
        """
        if isinstance(parent, Page):
            return parent.create_new_page(properties=properties, children=children, icon=icon, cover=cover)

    def create_new_database(self,
        parent: Union[Page, Parent],
        title: Union[DatabaseTitle, str] = DatabaseTitle("new database"),
        properties: Union[Properties, dict] = Properties(),
        icon: Union[Emoji, str] = Emoji('🐧'),
        cover: Union[File, str] = None):
        if isinstance(title, str):
            title = DatabaseTitle(title)
        database_object = DatabaseObject(
            parent=Parent(parent),
            title=title,
            properties= properties,
            icon=icon,
        )
        #print(database_object.make())
        r = requests.post(BaseObject.DatabaseAPI, headers=self.headers, json=database_object.make())
        if r.status_code == 200:
            return Database(self, r.json()['id'])
        else:
            return r.json()


if __name__ == '__main__':
    notion_bot = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
    test_page = notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')
    # db = notion_bot.get_database('ad29cd8f20584c1d98d33bf9e70c5377')
    db = notion_bot.create_new_database(
        parent=test_page,
        title="Hello",
        properties=Properties(
            name=TitleProperty(),
            test=TextProperty(),
        )
    )
    print(db.retrieve())
    # # p = Properties(title=TitleValue('Hello'))
    # # print(p.make())
    # test = notion_bot.create_new_page(
    #     parent=test_page,
    #     properties=Properties(
    #         title=TitleValue('Hello')
    #     ),
    #     icon=Emoji('🐒')
    # )
    # test.restore()
    #print(test_page.retrieve())
    # print(test_page.retrieve_property_item())
    # notion_bot.create_new_page(parent=test_page, properties=Properties())

    #
    # @classmethod
    # def retrieve_from(cls, target: Union[Page, Database, Block]):
    #     return target.retrieve()
    #
    # @staticmethod
    # def create_new_page(parent: Union[Page, Database], content: PageObject):
    #     if isinstance(parent, Database):
    #         return parent.post(parent.new_page(content))
    #
    #     elif isinstance(parent, Page):
    #         return parent.create_page(content)
    #
    # def fetch_databases(self, title: str):
    #     payload = {
    #         'query': f'{title}',
    #         'filter': {'value': 'database', 'property': 'object'},
    #         'page_size': 100
    #     }
    #     response = requests.request("POST", self.search_api, json=payload, headers=self.patch_headers)
    #     if response.json()['results']:
    #         text = response.json()['results'][0]
    #         database_id = text['id']
    #         print(f"fetching database {title} successfully")
    #         return Database(bot=self, database_id=database_id)
    #
    #     else:
    #         print(f"Can't find database {title}, check if it exist in your notion page")
    #
    # def fetch_page(self, title):
    #     payload = {
    #         'query': f'{title}',
    #         'filter': {'value': 'page', 'property': 'object'},
    #         'page_size': 100
    #     }
    #     response = requests.post(self.search_api, json=payload, headers=self.patch_headers)
    #     # print(response.json())
    #     if response.status_code == 200:
    #         # print(response.text)
    #         text = response.json()['results'][0]
    #         page_id = text['id']
    #         # print(page_id)
    #         print(f"fetch {title} page successfully")
    #         return Page(page_id=page_id, bot=self)
    #     else:
    #         print(f"Can't find page {title}")
    #
    #     return None
    #
    # def append_block(self, target_page: Page, children_array):
    #     target_page.append_children(children_array)
    #
    # def update_page(self, target, data):
    #     if isinstance(target.parent, Database):
    #         data = target.parent.new_page(data)
    #     target.update(data)
    #
    # def create_new_database(self, parent: Page, title=None, properties=None, icon=None, cover=None, is_inline=False):
    #     r = parent.create_database(title=title, properties=properties, icon=icon, cover=cover, is_inline=is_inline)
    #     if r.status_code == 200:
    #         print(f"create_new_database successfully id {r.json()['id']} ")
    #         return Database(self, r.json()['id'])
    #     else:
    #         print(r.json()['message'])


