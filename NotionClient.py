from PyNotion import *
from PyNotion import Database,Page


class Notion:
    def __init__(self,auth):
        self.auth = auth
        self.url = f'https://api.notion.com/v1'
        self.search_url = self.url + "/search"
        self.search_database = self.url + "/databases?page_size=100"
        self.headers = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": "2021-08-16",
            "Accept": "application/json",
        }
        self.patch_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json"
        }

    def fetch_databases(self,title):
        payload = {
            'query':f'{title}',
            'filter':{'value':'database','property':'object'},
            'page_size':100
        }
        response = requests.request("POST", self.search_url,json=payload,headers=self.patch_headers)
        #print(response.json())
        if response.json()['results']:
            #print(response.text)
            text = response.json()['results'][0]
            database_id = text['id']
            #page_id = text['parent']['page_id']
            #print(page_id)
            #page = Page(page_id=page_id,Bot=self)
            return Database(database_id=database_id,Bot=self)
        else:
            print(f"Can't find DataBase {title}")
            return None

    def fetch_page(self,title):
        payload = {
            'query': f'{title}',
            'filter': {'value': 'page', 'property': 'object'},
            'page_size': 100
        }
        response = requests.request("POST", self.search_url, json=payload, headers=self.patch_headers)
        #print(response.json())
        if response.json()['results']:
            # print(response.text)
            text = response.json()['results'][0]
            page_id = text['id']
            # print(page_id)
            return Page(page_id=page_id, Bot=self)
        else:
            print(f"Can't find Page {title}")

        return None

    def create_new_page(self, data, database=None):
        if database:
            p = Page.create_page(self,database.make_post(data))
        else:
            p = Page.create_page(self, data)
        return p

    def append_block(self,target_page,children_array):
        pass




if __name__ == '__main__':
    notion = Notion("secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
    #d = notion.fetch_databases('EECLASS')
    #print(d.properties)
    page3 = page.Page(page_id="e863ab46-2963-40c9-992c-465a78b3db3b",Bot=notion)
