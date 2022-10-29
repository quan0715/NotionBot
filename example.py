import PyNotion
from NotionClient import Notion
from database import *
import pandas as pd
notion = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
eeclass_db = notion.fetch_databases("EECLASS")
query = Query(sorts=[SortObject(prop="Sorts")])
print(eeclass_db)
# pl = eeclass_db.query_database_page_list()
# for page in pl:
#     print(page)
df = pd.DataFrame(eeclass_db.query_database_dataframe())
df = df[['標題', '類型', '連結']]
print(df.to_markdown())
