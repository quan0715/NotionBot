from NotionClient import Notion


def create_notion_bot():
    notion = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
    r = notion.bot_user()
    return r['object'] if r else False


def main():
    print(create_notion_bot())


if __name__ == "__main__":
    main()