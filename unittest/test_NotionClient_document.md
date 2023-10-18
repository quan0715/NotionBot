# Unit Test Document of NotionBot.NotionClient

## Introduction
This document outlines the unit testing structure, methods, test cases of [test_Notion_Client.py](./test_NotionClient.py).

## Test Execution
To run the tests, navigate under 'NotionBot' folder, and use the following command.

```sh
pip install pytest
pytest unittest/*
```

## Detail Test Plan

### Function 1: `Notion.get_user()`
- **Description:** This function gets the user information from a given auth token.
- **Test Cases:**
   1. `test_get_existing_user` : Test with a valid auth token.
   2. `test_get_non_existing_user` : Test with a invalid auth token.

### Function 2: `Notion.search()`
- **Description:** This function search a certain elements within a Notion integration connection.
- **Test Cases:**
   1. `test_search_valid_object` : Test with searching a valid target.
   2. `test_search_invalid_object` : Test with searching an invalid target.

### Function 3: `Notion.get_block`
- **Description:** This function finds the maximum value in a list.
- **Test Cases:**
   1. `test_get_existing_block` : Test with a valid block_id.
   2. `test_get_non_existing_block` : Test with an invalid block_id.

### Function 4: `Notion.get_page`
- **Description:** This function finds the maximum value in a list.
- **Test Cases:**
   1. `test_get_existing_page` : Test with a valid page_id.
   2. `test_get_non_existing_page` : Test with an invalid page_id.

### Function 5: `Notion.get_database`
- **Description:** This function finds the maximum value in a list.
- **Test Cases:**
   1. `test_get_existing_database` :Test with a valid database_id.
   2. `test_get_non_existing_database` : Test with an invalid database_id.

### Function 6: `Notion.create_new_page`
- **Description:** This function creates new database within Page, Database or Parent.
- **Test Cases:**
   1. `test_create_new_page_success` : POST status code return 200.
   2. `test_create_new_page_failure` : POST status code return 400.

### Function 7: `Notion.create_new_database`
- **Description:** This function creates new database within Page or Parent.
- **Test Cases:**
   1. `test_create_new_database_success` : POST status code return 200.
   2. `test_create_new_database_failure` : POST status code return 400.
