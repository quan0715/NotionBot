
from PyNotion import *
import PyNotion.template as tp

class Block:
    def __init__(self,block_id,parent):
        self.block_id = block_id
        self.parent = parent
        self.url = f'https://api.notion.com/v1/pages/'
        self.block_url = f'https://api.notion.com/v1/blocks/{self.block_id}'
    def retrieve_block(self):
        r = requests.get(self.block_url, headers=self.parent.patch_headers)
        return r.json()


class CodeBlock(Block):
    def __init__(self, block_id,parent):
        super().__init__(block_id, parent)
        self.property = self.retrieve_block()
        self.word = self.property['code']['text'][0]['text']['content']
        self.language = self.property['code']['language']
        #self.language = "plain text"
        self.template = {'code': self.property['code']}

    def update_block(self, text, language=None, cover=False):
        self.word = text if cover else self.word + text
        if language:
            self.language = language
        self.template['code']['text'][0]['text']['content'] = f"{self.word}"
        self.template['code']['language'] = f"{self.language}"
        r = requests.patch(self.block_url, headers=self.parent.patch_headers, data=json.dumps(self.template))
        #print(self.template)
        print(r.text)

    def clear_block(self):
        self.template = tp.code_block_template
        self.property = self.retrieve_block()
        self.word = self.property['code']['text'][0]['text']['content']
        self.language = self.property['code']['language']
        requests.patch(self.block_url, headers=self.parent.patch_headers, data=json.dumps(self.template))






class Embed_block(Block):
    def __init__(self, block_id, parent,embed_url):
        super().__init__(block_id, parent)
        self.embed_url = embed_url
        self.template = {
            "type": "embed",
            "embed": {
                "url": f"{self.embed_url}"
            }
        }

    def update_url(self, url):
        self.embed_url = url
        self.template['embed']['url'] = self.embed_url
        requests.patch(self.block_url, headers=self.parent.patch_headers, data=json.dumps(self.template))
