from PyNotion.object import *


class Block(BaseObject):
    def __init__(self, bot, block_id):
        super().__init__(bot, block_id)
        self.block_url = BaseObject.BlockAPI + self.object_id
        self.children_url = f'{self.block_url}/children'

    def retrieve(self, **kwargs):
        return super().retrieve(self.block_url)

    def update(self, data, **kwargs):
        return super().update(self.block_url, data)