import unittest

from PyNotion.NotionClient import Notion
from PyNotion.object import *
from PyNotion.base import *


class DatabaseTest(unittest.TestCase):
    def setUp(self):  # will be called before each testcase startup
        self.notion_bot = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
        self.database = self.notion_bot.get_database('ad29cd8f20584c1d98d33bf9e70c5377')
        self.page = self.notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')

    def tearDown(self):  # will be called in end of the test case
        self.notion_bot = None
        self.database = None
        self.page = None

    def test_update_database(self):
        db = self.notion_bot.create_new_database(
            parent=self.page,
            title=Texts('Hello'),
            properties=Properties(
                title=TitleProperty(),
                l_b=LastEditedByProperty(),
                l_t=LastEditedTimeProperty(),
                c_b=CreatedByProperty(),
                c_t=CreatedTimeProperty()
            )
        )
        # print("before update")
        # print(db.print_properties())
        result = db.update(
            title=Texts('Hello'),
            properties=Properties(
                Test=TextProperty(),
                Test_clear=TextProperty(),
                url=UrlProperty(),
                number=NumberProperty(),
            )
        )
        # print("after update")
        # print(db.print_properties())
        self.assertTrue(isinstance(result, dict))
        result = db.update(
            description=Texts('Test description\n', 'beautiful\n'),
            title=Texts('Hello'),
            properties=Properties(
                Test_clear=None,
                # number_change_name=PropertyName('number_change')
            )
        )
        self.assertTrue(isinstance(result, dict))

    def test_database_new_page(self):
        result = self.database.create_new_page(
            properties=Properties(
                Test=TextValue('text'),
                Name=TitleValue('text'),
                number=NumberValue(123),
            )
        )
        self.assertTrue(isinstance(result, Page))

    def test_database_query(self):
        result = self.database.query()
        self.assertTrue(isinstance(result, list))


if __name__ == '__main__':
    unittest.main()
