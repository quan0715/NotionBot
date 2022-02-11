from PyNotion import *


class Page:
    def __init__(self, token, page_id):
        self.token = token
        self.page_id = page_id
        self.url = f'https://api.notion.com/v1/pages/'
        self.search_url = "https://api.notion.com/v1/search"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2021-08-16"
        }
        self.patch_headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json"
        }
        self.parent_json = {
            "parent": {
                "type": "page_id",
                "page_id": self.page_id
            }
        }

    # def create_database(self):


    def get_database_id(self, target):
        r = requests.post(self.search_url, headers=self.patch_headers)
        print(target)
        j = json.loads(r.text)
        results = j['results']
        for r in results:
            if r['object'] == 'database' and r['title'][0]['text']['content'] == target:
                return r['id']
        return False
