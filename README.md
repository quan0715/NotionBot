# PyNotion

## 使用教學

### Create your own Integration

### Start using PyNotion
```python3
from PyNotion.NotionClient import Notion
AUTH = "secret_6Dxn84zjANca6LHA6jXuY1gOlcqXzQttl3kGZKNPemh" #your own integration's token
notion_bot = Notion(auth=AUTH)
```
If it authenticated, it will print out `Connect to integration Quan`,otherwise `Connect failed please request again !!!`
As you run into this situation, make sure to check out your integration token is type it correctly.

### 讀取特定的page或database
#### Notion.fetch_page(your page title)
```python3
main_page = notion_bot.fetch_page("PyNotion test")
```

