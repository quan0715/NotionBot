from PyNotion import *
from PyNotion import Database, Page
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
        if response.status_code == 200:
            # print(response.text)
            text = response.json()['results'][0]
            page_id = text['id']
            # print(page_id)
            print(f"fetch {title} Page successfully")
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

    def create_new_database(self, title: str, parent: Page, properties: PropertyObject):
        """
        :param title: str object, set the title of the database, request
        :param icon : icon of your database
        :param parent: Page, set the database parent in which page
        :param properties: PropertyObject: properties name and their corresponding value type
        """
        template = {
            "parent": ParentObject(parent_type=ParentType.page_id, parent_id=parent.object_id).template,
            "title": TextObject(content=title).template,
            "properties": properties.get_template(),
        }
        #print(template)
        r = requests.post(Database.database_api, headers=self.patch_headers, data=json.dumps(template))
        if r.status_code == 200:
            print(f"database {title} 創建成功,你可以在 page_id {parent.object_id} 找到他")
            return r.json()
        else:
            print(r.json()['message'])