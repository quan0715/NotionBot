import unittest

from NotionClient import Notion
from base import *
from object import *

class NotionClientTest(unittest.TestCase):
    def setUp(self): # will be called before each testcase startup
        self.notion_bot = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")

    def tearDown(self): # will be called in end of the test case
        self.notion_bot = None

    def test_fetch_user(self):
        expected_type = "user"
        result = self.notion_bot.get_user()
        object_type = result['object']
        self.assertEqual(expected_type, object_type)

    def test_fetch_block(self):
        result = self.notion_bot.get_block('91aecee505504440936ca0154974ea93')
        self.assertEqual(True, isinstance(result, Block))

    def test_fetch_page(self):
        result = self.notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')
        self.assertEqual(True, isinstance(result, Page))

    def test_create_new_page(self):
        test_page = self.notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')
        result = self.notion_bot.create_new_page(
            parent=test_page,
            properties=Properties(title=TitleValue('Hello')),
            icon=Emoji('🐒')
        )
        self.assertEqual(True, isinstance(result, Page))

    def test_fetch_database(self):
        result = self.notion_bot.get_database('ad29cd8f20584c1d98d33bf9e70c5377')
        self.assertEqual(True, isinstance(result, Database))

    def test_create_database(self):
        test_page = self.notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')
        result = self.notion_bot.create_new_database(
            parent=test_page,
            title=Texts('hey', 'hi'),
            properties=Properties(
                name=TitleProperty(),
                test=TextProperty(),
            ),
            description = Texts('Hello', 'hhhhhh\n\n\n'),
            icon = Emoji('🐧')
        )
        self.assertEqual(True, isinstance(result, Database))

    def test_search(self):
        expected_type = "list"
        result = self.notion_bot.search('PyNotion test')
        object_type = result['object']
        self.assertEqual(expected_type, object_type)




if __name__ == '__main__':
    unittest.main()
