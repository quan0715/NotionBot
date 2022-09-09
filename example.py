from PyNotion import *
from NotionClient import *
import os
from dotenv import load_dotenv
import pandas as pd

notion = Notion(auth="secret_8JtNxNiUCCWPRhFqzl1e2juzxoz96dyjYWubDLbNchy")
schedule_db = notion.fetch_databases("課表")
print(schedule_db)
df = pd.DataFrame(schedule_db.query_database_dataframe())
print(df.to_markdown())
