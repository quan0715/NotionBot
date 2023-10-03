# NotionBot
## Introducing to NotionBot

NotionBot SDK is a user-friendly toolkit designed to simplify interactions with the official Notion API. It empowers developers to easily integrate Notion's features into their applications.

## How to use it

### Create your own Integration
* Create an integration in order to provide an interface for API to identify your Notion contents.
* Official documentation : [https://developers.notion.com/docs/create-a-notion-integration](https://developers.notion.com/docs/create-a-notion-integration)

### Install NotionBot Package
```sh
git clone https://github.com/quan0715/NotionBot.git
cd NotionBot
pip install .
```

### Start using NotionBot in your Python script
```python3
from NotionBot.NotionClient import Notion
AUTH = <your own integration's token>
notion_bot = Notion(auth=AUTH)
```
* Integration token usually started with "secret_..."
* If it authenticated, it will print out `Connect to integration YOUR_INEGRATION_NAME`,otherwise `Connect failed please request again !!!`
As you run into this situation, make sure to check out your integration token is type it correctly.

### Get specific Page, Database, Block
#### Notion.get_page(your page title)

```python3
page = your_notion_bot.get_page("your_page_title")
```
#### Notion.get_database(your page title)
```python3
database = your_notion_bot.get_page("your_database_title")
```
###
```python3
block = your_notion_bot.fetch_block("your_block_id")
```


