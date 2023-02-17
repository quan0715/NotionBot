from enum import Enum
from .NotionObject import *
from typing import List, Union


class RelationProperty(PropertyBase):
    def __init__(self, database, relation_type):
        super().__init__("relation")
        self.database_id = database.object_id
        self.relation_type = relation_type
        self.template[self.type].update(dict(
            database_id=self.database_id
        ))
        self.template[self.type].update(self.relation_type.make())
        print(self.template)


class SingleRelation(PropertyBase):
    def __init__(self):
        super().__init__("single_property")


class DualRelation(PropertyBase):
    def __init__(self):
        super().__init__("dual_property")
        #self.template[self.type].update({"synced_property_name": "Fuck"})


class RelationValue:
    def __init__(self, page_id: List[str]):
        self.template = {"relation": [{p_id} for p_id in page_id]}
