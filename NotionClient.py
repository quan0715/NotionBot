from PyNotion import *
from PyNotion import Database, Page
from PyNotion.BaseObject import *
from PyNotion.Object import *


class Notion:
    user_api = "https://api.notion.com/v1/users/me"

    def __init__(self, auth):
        """
        :param auth: your notion integration internal token
        """
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

    def fetch_databases(self, title, page_size=1):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'database', 'property': 'object'},
            'page_size': page_size
        }
        response = requests.request("POST", self.search_url, json=payload, headers=self.patch_headers)
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

    def fetch_page(self, title, page_size=1):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'page', 'property': 'object'},
            'page_size': page_size
        }
        response = requests.post(self.search_url, json=payload, headers=self.patch_headers)
        # print(response.json())
        if response.status_code == 200:
            #print(response.text)
            text = response.json()['results'][0]
            page_id = text['id']
            # print(page_id)
            print(f"fetch {title} Page successfully")
            return Page(page_id=page_id, bot=self)
        else:
            print(f"Can't find Page {title}")

        return None

    def fetch_block(self, block_id):
        if block_id.startswith("https://www.notion.so/"):
            block_id = block_id.split("#")[-1]
        return Block(bot=self, block_id=block_id)

    def create_new_page(self, data, database=None):
        if database:
            p = database.post(database.post_template(data))
        else:
            p = Page.create_page(self, data)
        return p

    def append_block(self, target_page, children_array):
        pass

    def update_page(self,target, data):
        if isinstance(target.parent, Database):
            data = target.parent.post_template(data)
        target.update(data, )


    def create_new_database(self, title: str, parent: Page, property_object):
        """
        :param property_object: PropertyObject: properties name and their corresponding value type
        :param title: str object, set the title of the database, request
        :param parent: Page, set the database parent in which page
        """
        template = {
            "parent": ParentObject(parent_type=ParentType.page_id, parent_id=parent.object_id).template,
            "title": TextObject(content=title).template,
        }
        if isinstance(property_object, PropertyObject):
            template.update(dict(properties=property_object.get_template()))
        else:
            template.update(dict(properties=PropertyObject({"UnTitle": TitleProperty()}).get_template()))
        #print(template)
        #print(template)
        r = requests.post(BaseObject.DatabaseAPI, headers=self.patch_headers, data=json.dumps(template))
        if r.status_code == 200:
            print(f"database {title} 創建成功,你可以在 page_id {parent.object_id} 找到他")
            return r.json()
        else:
            print(r.json()['message'])