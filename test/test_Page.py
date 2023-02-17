import unittest

from NotionClient import Notion
from base import *
from object import *


class PageTest(unittest.TestCase):
    def setUp(self):  # will be called before each testcase startup
        self.notion_bot = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
        self.page = self.notion_bot.get_page('3be396829d3149b2818a4957ff878bf9')

    def tearDown(self):  # will be called in end of the test case
        self.notion_bot = None
        self.page = None

    # def test_create_new_page(self):
    #     result = self.page.create_new_page(
    #         properties=Properties(title=TitleValue("Hello"))
    #     )
    #     self.assertTrue(isinstance(result, Page))

    def test_update_page(self):
        p = self.page.create_new_page()
        result = p.update(icon=Emoji('🐶'))
        self.assertTrue(isinstance(result, dict))


if __name__ == '__main__':
    unittest.main()
