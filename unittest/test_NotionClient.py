import pytest
from unittest.mock import Mock, patch
from NotionBot.NotionClient import Notion, Page, Database, Block
import os
from NotionBot.base import *
from NotionBot.object import *

# Create a mock(stub) to avoid sending requests to NotionAPI
@pytest.fixture
def mock_requests():
    with patch('NotionBot.NotionClient.requests') as mock_requests:
        yield mock_requests

# Test cases for the Notion class
class TestNotion:

    @pytest.fixture
    def notion_client(self, mock_requests):
        auth_token = "secret_this_is_a_valid_notion_api_token"
        notion = Notion(auth=auth_token)
        return notion

    def test_get_user(self, notion_client, mock_requests):

        # Mock the requests.get method
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"name": "Test User"}
        
        user = notion_client.get_user()
        assert user == {"name": "Test User"}

        # Ensure that the requests.get method was called with the correct URL and headers
        mock_requests.get.assert_called_once_with(
            "https://api.notion.com/v1/users/me",
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
        )

    def test_search(self, notion_client, mock_requests):
        
        search_result = {"results": [{"name": "Test search results"}]}
        target = "test_target"

        # Mock the requests.post method
        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {"results": [{"name": "Test search results"}]}

        result = notion_client.search(target)
        assert result == search_result

        # Ensure that the requests.post method was called with the correct URL, headers, and payload
        mock_requests.post.assert_called_once_with(
            "https://api.notion.com/v1/search",
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
            json={"query": target, "page_size": 100},
        )

    def test_get_block(self, notion_client, mock_requests):
        block_id = "block_id"

        # Mock the requests get method
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"id": "test_block_id"}

        block = notion_client.get_block(block_id)

        # Check if the returned block is an instance of the Block class
        assert isinstance(block, Block)

        # Ensure that the requests.get method was called with the correct URL and headers
        mock_requests.get.assert_called_once_with(
            f"https://api.notion.com/v1/blocks/{block_id}",
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
        )

    def test_get_database(self, notion_client, mock_requests):
        # Mock the requests get method
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"id": "test_database_id"}

        database_id = "database_id"
        database = notion_client.get_database(database_id)

        # Check if the returned database is an instance of the Database class
        assert isinstance(database, Database)

        # Ensure that the requests.get method was called with the correct URL and headers
        mock_requests.get.assert_called_once_with(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
        )

    def test_create_new_page(self, notion_client, mock_requests):
        parent_page = Page(page_id="parent_page_id")  # Create a mock parent page for testing
        properties = Properties(title="Test Page")

        # Mock the requests.post method for create_new_page
        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {"id": "new_page_id"}

        new_page = notion_client.create_new_page(parent_page, properties)

        # Check if the returned object is an instance of the Page class
        assert isinstance(new_page, Page)

        # Ensure that the requests.post method was called with the correct URL, headers, and payload
        mock_requests.post.assert_called_once_with(
            Database.PageAPI,
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
            json={
                "parent": {"page_id": "parent_page_id"},
                "properties": properties.to_dict()  # Use the to_dict method to convert Properties object to a dictionary
            },
        )

    def test_create_new_database(self, notion_client, mock_requests):
        parent_page = Page(page_id="parent_page_id")  # Create a mock parent page for testing
        properties = Properties(title="Test Database")

        # Mock the requests.post method for create_new_database
        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {"id": "new_database_id"}

        new_database = notion_client.create_new_database(parent_page, properties)

        # Check if the returned object is an instance of the Database class
        assert isinstance(new_database, Database)

        # Ensure that the requests.post method was called with the correct URL, headers, and payload
        mock_requests.post.assert_called_once_with(
            Database.DatabaseAPI,
            headers={"Authorization": f"Bearer {notion_client.auth}", "Notion-Version": Notion.notion_version, "Accept": "application/json"},
            json={
                "parent": {"page_id": "parent_page_id"},
                "properties": properties.to_dict()  # Use the to_dict method to convert Properties object to a dictionary
            },
        )

# if __name__ == "__main__":
#     TestNotion.test_get_block()