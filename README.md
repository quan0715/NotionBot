# PyNotion

## 使用教學

### Create your own Integration

### Start using PyNotion
```python3
from PyNotion.NotionClient import Notion
AUTH = "your own integration's token"
notion_bot = Notion(auth=AUTH)
```
If it authenticated, it will print out `Connect to integration YOUR_INEGRATION_NAME`,otherwise `Connect failed please request again !!!`
As you run into this situation, make sure to check out your integration token is type it correctly.

### Fetch specific page or database
#### Notion.fetch_page(your page title)
```python3
page = your_notion_bot.fetch_page("your_page_title")
```
#### Notion.fetch_database(your page title)
```python3
database = your_notion_bot.fetch_page("your_data_base_title")
```

