"""
File: 
    test_NotionClient.py
Description:
    Test member functions inside Notion class in NotionClient.py with high test isolation.
"""
import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from NotionBot.NotionClient import Notion
import os
from NotionBot.base import *
from NotionBot.object import *

# Create a mock(stub) to avoid sending requests to Notion API
@pytest.fixture
def mock_requests():
    with patch('NotionBot.NotionClient.requests') as mock_requests:
        yield mock_requests

# Create a mock(stub) to avoid sending requests to Notion class constructor
@pytest.fixture
def notion_client(mock_requests):
    auth_token = "secret_this_is_an_api_token"
    notion = Notion(auth=auth_token)
    return notion

# Test cases for the NotionClient.Notion class
class TestNotion():

    def test_get_user_success(self, notion_client, mock_requests):

        # Mock the requests.get method
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"name": "Test User"}
        
        user = notion_client.get_user()
        assert user == {"name": "Test User"}

        # Ensure that the requests.get method was called once with the correct information
        mock_requests.get.assert_called_once_with(
            "https://api.notion.com/v1/users/me",
            headers=notion_client.headers
        )

    def test_get_user_failure(self, notion_client, mock_requests):

        # Mock the requests.get method
        mock_requests.get.return_value.status_code = 400
        mock_requests.get.return_value.json.return_value = {'message': 'Failed'}
        
        user = notion_client.get_user()
        assert user == 'Failed'

        # Ensure that the requests.get method was called once with the correct information
        mock_requests.get.assert_called_once_with(
            "https://api.notion.com/v1/users/me",
            headers=notion_client.headers
        )

    def test_search(self, notion_client, mock_requests):
        
        search_result = {"results": [{"name": "Test search results"}]}
        target = "test_target"

        mock_requests.post.return_value.status_code = 200
        mock_requests.post.return_value.json.return_value = {"results": [{"name": "Test search results"}]}

        result = notion_client.search(target)
        assert result == search_result

        mock_requests.post.assert_called_once_with(
            "https://api.notion.com/v1/search",
            headers=notion_client.headers,
            json={"query": target, "page_size": 100},
        )

    def test_get_block(self, notion_client, mock_requests):
        block_id = "block_id"

        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"id": "test_block_id"}

        block = notion_client.get_block(block_id)

        assert isinstance(block, Block)

        mock_requests.get.assert_called_once_with(
            f"https://api.notion.com/v1/blocks/{block_id}",
            headers=notion_client.headers
        )

    def test_get_database(self, notion_client, mock_requests):

        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {"id": "test_database_id"}

        database_id = "database_id"
        database = notion_client.get_database(database_id)

        # Check if the returned database is an instance of the Database class
        assert isinstance(database, Database)

        mock_requests.get.assert_called_once_with(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=notion_client.headers
        )

class TestCreatPage(unittest.TestCase):

    @patch('NotionBot.NotionClient.requests')
    def test_create_new_page_success(self, mock_requests):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'mocked_page_id'}

        mock_requests.post.return_value = mock_response

        notion = Notion(auth='secret_this_is_an_api_token')

        # Create a mock parent object
        mock_parent = MagicMock()
        mock_parent.object_id = 'mocked_parent_id'

        new_page = notion.create_new_page(parent=mock_parent)

        # Assertions
        mock_requests.post.assert_called_with(
            'https://api.notion.com/v1/pages/',
            headers=notion.headers,
            json=mock_requests.post.call_args[1]['json']
        )
        self.assertIsInstance(new_page, Page)
    
    @patch('NotionBot.NotionClient.requests')
    def test_create_new_page_failure(self, mock_requests):

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'message': 'Failed'}

        mock_requests.post.return_value = mock_response

        notion = Notion(auth='secret_this_is_an_api_token')

        mock_parent = MagicMock()
        mock_parent.object_id = 'mocked_parent_id'

        result = notion.create_new_page(parent=mock_parent)

        # Assertions
        mock_requests.post.assert_called_with(
            'https://api.notion.com/v1/pages/',
            headers=notion.headers,
            json=mock_requests.post.call_args[1]['json']
        )
        self.assertEqual(result, 'Failed')


class TestCreateDatabase(unittest.TestCase):

    @patch('NotionBot.NotionClient.requests')
    def test_create_new_database_success(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'mocked_database_id'}

        mock_requests.post.return_value = mock_response

        notion = Notion(auth='secret_this_is_an_api_token')

        bot = MagicMock()
        database = Database(bot=bot, database_id='mocked_database_id')

        new_database = notion.create_new_database(parent=bot)

        mock_requests.post.assert_called_with(
            'https://api.notion.com/v1/databases/',
            headers=notion.headers,
            json=mock_requests.post.call_args[1]['json']
        )
        self.assertIsInstance(new_database, Database)

    @patch('NotionBot.NotionClient.requests')
    def test_create_new_database_failure(self, mock_requests):

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'message': 'Failed'}

        mock_requests.post.return_value = mock_response

        notion = Notion(auth='secret_this_is_an_api_token')
        
        bot = MagicMock()
        database = Database(bot=bot, database_id='mocked_database_id')

        result = notion.create_new_database(parent=bot)

        mock_requests.post.assert_called_with(
            'https://api.notion.com/v1/databases/',
            headers=notion.headers,
            json=mock_requests.post.call_args[1]['json']
        )
        self.assertEqual(result, {'message': 'Failed'})
