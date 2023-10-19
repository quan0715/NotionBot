># NotionBot SDK Guide

|Guide|Description|
|-|-|
|[Notion Class](#notion-class)|A class that enable developers to create a client side Notion object and assign specific tasks(e.g. search, create database...etc) to it.|
|[Base Class](#base-class)|A base class for [Database](#database-class), [Page](#page-class), and [Block](#block-class) class, provide them some basic features.|
|[Page Class](#page-class)|A class that provides methods and functionality for interacting with Notion pages.|
|[Block Class](#block-class)||
|[Database Class](#database-class)||

# Notion Class
[[Back to top]](#notionbot-sdk-guide)

A class that enable developers to create a client side Notion object and assign specific tasks(e.g. search, create database…etc) to it.

## `Notion(auth)`

#### Description

Constructor of the `Notion` object.

#### Parameters
- `auth`: Your Notion integration internal token.

#### Return Value

- If the request succeeds, it will create a `Notion` object, allowing you to perform various Notion-related operations.
- If the request fails, it will print an error message and return it.

## `Notion.get_user()`

#### Description

Retrieves information about the current user.

#### Return Value

- If the request succeeds, it will return information about the user.
- If the request fails, it will print an error message and return it.

## `Notion.search(target: str = None)`

#### Description

Search for a target database or page.

#### Parameters
- `target`: The name of the target database or page.

#### Return Value

- If the request succeeds, it will return a JSON file representing the list of search results.
- If the request fails, it will print an error message and return it.

## `Notion.get_block(block_id) -> Block`

#### Description

Retrieves information about a specific block.

#### Parameters
- `block_id`: The ID of a specific block in a Notion page.

#### Return Value

- If the request succeeds, it will return a `Block` object representing the block.
- If the request fails, it will print an error message and return it.

## `Notion.get_page(page_id) -> Page`

#### Description

Retrieves information about a specific page.

#### Parameters
- `page_id`: The ID of a specific page on your Notion workspace.

#### Return Value

- If the request succeeds, it will return a `Page` object representing the page.
- If the request fails, it will print an error message and return it.

## `Notion.get_database(database_id)`

#### Description

Retrieves information about a specific database.

#### Parameters
- `database_id`: The ID of a specific database in a Notion page.

#### Return Value

- If the request succeeds, it will return a `Database` object representing the database.
- If the request fails, it will print an error message and return it.

## `Notion.create_new_page(parent: Union[Page, Database, Parent], properties: Union[Properties, dict] = Properties(), **kwargs)`

#### Description

Creates a new page within the current page or database.

#### Parameters
- `parent`: Information about the page's parent, represented as a JSON object with a `page_id` or `database_id` key, and the corresponding ID.
- `properties`: The schema of properties, using a [Properties object](../NotionBot/object/Properties.py) to implement a predefined JSON template.
- `**kwargs`: Additional keyword arguments for customizing the new page.

#### Return Value

- If the request succeeds, it will return a new `Page` object representing the created page.
- If the request fails, it will print an error message and return it.

## `Notion.create_new_database(parent: Union[Page, Parent], properties: Union[Properties, dict] = Properties(), **kwargs)`

#### Description

Creates a new database within the current page.

#### Parameters
- `parent`: Information about the database's parent, represented as a JSON object with a `page_id` key and the corresponding ID.
- `properties`: The schema of properties, using a [Properties object](../NotionBot/object/Properties.py) to implement a predefined JSON template.
- `**kwargs`: Additional keyword arguments for customizing the new database.

#### Return Value

- If the request succeeds, it will return a new `Database` object representing the created database.
- If the request fails, it will print an error message and return it.

The `Notion` class provides methods for interacting with Notion objects and allows for the creation of new pages and databases within a Notion workspace.

# Base Class
[[Back to top]](#notionbot-sdk-guide)

A base class for [Database](#database-class), [Page](#page-class), and [Block](#block-class) class, provide them some basic features.

## `Base(bot, object_id, object)`

#### Description

Constructor of the `Base` object.

#### Parameters

- `bot`: Represents the Notion integration token. Ensure you have created your own Notion integration before using it. [Create a Notion integration](https://developers.notion.com/docs/create-a-notion-integration).
- `object_id`: Represents the unique identifier for the Notion object.
- `object`: Specifies the type of Notion object, which can be "database," "page," or "block."

#### Return Value

- If the request succeeds, it returns a `Base` object, which can be used for various operations.
- If the request fails, it prints an error message and returns the error.

## `Base.retrieve()`

#### Description

Retrieves details about the Notion object.

#### Return Value

- If the request succeeds, it returns a dictionary containing details about the object, including creation and last edit times, creators, and properties.
- If the request fails, it prints an error message and returns the error.

## `Base.print_properties()`

#### Description

Prints the properties of the Notion object.

#### Return Value

- If the request succeeds, it prints the properties of the object in a formatted manner.
- If the request fails, it prints an error message and returns the error.

## `Base.delete_object()`

#### Description

Deletes the Notion object.

#### Return Value

- If the request succeeds, it returns a confirmation message of the deletion.
- If the request fails, it prints an error message and returns the error.

## `Base.async_delete_object(session)`

#### Description

Asynchronously deletes the Notion object.

#### Parameters

- `session`: An asyncio session for making asynchronous requests.

#### Return Value

- If the request succeeds, it returns a confirmation message of the deletion as an awaitable.
- If the request fails, it prints an error message and returns the error as an awaitable.

## `Base.retrieve_children()`

#### Description

Retrieves children (blocks) of the Notion object.

#### Return Value

- If the request succeeds, it returns a JSON response containing the children (blocks).
- If the request fails, it prints an error message and returns the error.

## `Base.append_children(children: Children)`

#### Description

Appends children (blocks) to the Notion object.

#### Parameters

- `children`: An instance of the `Children` class representing the blocks to be added.

#### Return Value

- If the request succeeds, it returns a list of added children (blocks).
- If the request fails, it prints an error message and returns the error.

## `Base.async_append_children(children: Children, session)`

#### Description

Asynchronously appends children (blocks) to the Notion object.

#### Parameters

- `children`: An instance of the `Children` class representing the blocks to be added.
- `session`: An asyncio session for making asynchronous requests.

#### Return Value

- If the request succeeds, it returns a list of added children (blocks) as an awaitable.
- If the request fails, it prints an error message and returns the error as an awaitable.

The `Base` class provides a foundation for interacting with Notion objects and is used for tasks such as retrieving details, managing children, and deleting objects.

# Page Class
[[Back to top]](#notionbot-sdk-guide)

A class that provides methods and functionality for interacting with Notion pages.

## `Page(bot, page_id)`

#### Description

Constructor of the `Page` object.

#### Parameters
- `bot`: Represents the Notion integration token.
- `page_id`: Represents the unique identifier of the Notion page.

#### Return Value

- If the request succeeds, it will return a `Page` object, allowing you to perform various page-related operations.
- If the request fails, it will print an error message and return it.

## `Page.retrieve_property_item(property_id)`

#### Description

Retrieves information about a specific property of the page.

#### Parameters
- `property_id`: Represents the ID of a specific property of the page, you might want to use [Notion.get_page()](#notionget_pagepage_id---page) first to find the id from the JSON response.

#### Return Value

- If the request succeeds, it will return a JSON representation of the property.
- If the request fails, it will print an error message and return it.

## `Page.update(**kwargs)`

#### Description

Updates the page with the provided data.

#### Parameters
- `**kwargs`: Keyword arguments representing the properties to update.

#### Return Value

- If the request succeeds, it will return a JSON response with updated page data.
- If the request fails, it will print an error message and return it.

## `Page.delete()`

#### Description

Deletes the page.

#### Return Value

- If the request succeeds, it will return a JSON response indicating the page has been deleted.
- If the request fails, it will print an error message and return it.

## `Page.restore()`

#### Description

Restores a previously deleted page.

#### Return Value

- If the request succeeds, it will return a JSON response indicating the page has been restored.
- If the request fails, it will print an error message and return it.

## `Page.create_new_page(properties: Properties = Properties(), **kwargs)`

#### Description

Creates a new page within the current page or database.

#### Parameters
- `properties`: Represents the schema of properties, using a [Properties object](../NotionBot/object/Properties.py) to implement a predefined JSON template.
- `**kwargs`: Additional keyword arguments for customizing the new page.

#### Return Value

- If the request succeeds, it will return a new `Page` object representing the created page.
- If the request fails, it will print an error message and return it.

# Block Class

# Database Class