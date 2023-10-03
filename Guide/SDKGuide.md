># NotionBot SDK Guide

## Notion object

### Notion(auth)
* Constructor of the Notion object.
#### Parameters
* `auth` represents the Notion integration token.
* If you try this for the first time, please [create your own Notion integration](https://developers.notion.com/docs/create-a-notion-integration) first.

#### Return Value
* If the request succeeded, it will return a `Notion` object, you can check the member functions below.
* If the request failed, it will print error message and return it.

### Notion.get_user()
#### Parameters
* No parameter is needed.
* Make sure you have create a new Notion object with your integration token.
#### Return Value
* If the request succeeded, it will return json file which represent the list of search result.
* If the request failed, it will print error message and return it.

### Notion.search(target)

#### Parameters
* `target` represents the name of target [database](https://www.notion.so/help/intro-to-databases) or [page](https://www.notion.so/help/create-your-first-page).

#### Return Value
* If the request succeeded, it will return json file which represent the list of search result.
* If the request failed, it will print error message and return it.
* To check the json format returned, please visit [here](https://developers.notion.com/reference/post-search).

### Notion.get_block(block_id)
* [What is a block ?](https://www.notion.so/help/what-is-a-block)
#### Parameters
* `block_id` represents the id of a specific block in a Notion page.
* To see how to get an id of a specific block, visit [here](https://stackoverflow.com/questions/67618449/how-to-get-the-block-id-in-notion-api).
#### Return Value
* If the request succeeded, it will return a `Block` object. (see [Block](./NotionBot/base/Block.py) object)
* If the request failed, it will print error message and return it.

### Notion.get_page(page_id)

#### Parameters
* `page_id` represents the id of a specific page on your Notion workspace.
* To see how to get an id of a specific page, visit [here](https://help.answerly.io/other/how-to-find-a-page-id-from-a-page-in-notion).

#### Return Value
* If the request succeeded, it will return a `Page` obejct. (see [Page](./NotionBot/base/Page.py) object)
* If the request failed, it will print error message and return it.

### Notion.get_database(database_id)
#### Parameters
* `database_id` represents the id of a specific database in a Notion page.
* To see how to get an id of a specific database, visit [here](https://stackoverflow.com/questions/67728038/where-to-find-database-id-for-my-database-in-notion).

#### Return Value
* If the request succeeded, it will return a `Database` obejct. (see [Database](./NotionBot/base/Database.py) object)
* If the request failed, it will print error message and return it.
