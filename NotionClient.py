from PyNotion import *
from PyNotion.database import Database
from PyNotion.page import Page
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
            'page_size':100
        }
        response = requests.request("POST", self.search_url,json=payload,headers=self.patch_headers)
        if response.json()['results']:
            #print(response.text)
            text = response.json()['results'][0]
            database_id = text['id']
            page_id = text['parent']['page_id']
            #print(page_id)
            page = Page(page_id=page_id,Bot=self)
            database = Database(database_id=database_id,Bot=self,parent=page)
        else:
            print(f"Can't find DataBase {title}")
        return database


    def search(self):
        response = requests.request("POST", self.search_url, headers=self.patch_headers)
        print(response.text)


if __name__ == '__main__':
    notion = Notion("secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
    notion.fetch_databases('eeclass')
