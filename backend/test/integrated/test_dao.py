import json
from typing import Any
from mongomock import MongoClient
import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO
import unittest.mock as mock
from unittest.mock import patch

class TestIntegrated:
    """
    Testcases for the dao create method
    """
    Valid_users = [
        {"firstName": "Steven", "lastName": "Anderson", "email": "joe@bloggs.com", "tasks": [1, 2]},
        {"firstName": "John", "lastName": "Doe", "email": "john@doe.com", "tasks": [1, 2]}
    ]

    Invalid_uniqueItems = [
        {"firstName": "Steven", "lastName": "Anderson", "email": "joe@bloggs.com", "tasks": [1, 1]},
        {"firstName": "John", "lastName": "Doe", "email": "john@doe.com", "tasks": [1, 1]}
    ]

    Invalid_users_partials = [
        {"lastName": "Doe", "email": "joe@bloggs.com", "tasks": [3,4]},
        {"firstName": "Joe", "email": "joe@bloggs.com", "tasks": [1,2]},
        {"firstName": "Steven", "lastName": "Anderson", "tasks": [1,2]},
        {"firstName": "Steven", "lastName": "Anderson", "email": "joe@bloggs.com"},
    ]

    Invalid_Data_Types = [
        {"firstName": True, "lastName": "Bloggs", "email": "joe@bloggs.com", "tasks": [1,2]},
        {"firstName": "Joe", "lastName": True, "email": "joe@bloggs.com", "tasks": [1,2]},
        {"firstName": "Steven", "lastName": "Anderson", "email": True, "tasks": [1,2]},
        {"firstName": "Steven", "lastName": "Anderson", "email": "joe@bloggs.com", "tasks": True}
    ]

    @pytest.fixture(scope="module")
    def sut(self):
        """Fixture for creating the System Under Test (SUT) with mocked validators."""
        # Load the JSON validator configuration
        with open('./test.json', 'r') as f:
            validator = json.load(f)
        
        # Mock the getValidator function to return the mock validator
        with patch('src.util.dao.getValidator', autospec=True) as mock_getValidator:
            mock_getValidator.return_value = validator
            sut = DAO('test')
            yield sut
            sut.collection.drop()

    @pytest.mark.integration
    @pytest.mark.parametrize("user", Invalid_Data_Types)
    def test_invalid_Data_Types(self, sut: DAO, user: Any):
        with pytest.raises(WriteError):
            sut.create(user)
    
    @pytest.mark.integration
    @pytest.mark.parametrize("user", Invalid_users_partials)
    def test_invalid_users_partials(self, sut: DAO, user: Any):
        with pytest.raises(WriteError):
            sut.create(user)

    @pytest.mark.integration
    @pytest.mark.parametrize("user", Invalid_uniqueItems)
    def test_invalid_unique_items(self, sut: DAO, user: dict[str, Any]):
        with pytest.raises(WriteError):
            sut.create(user)
    
    @pytest.mark.integration
    @pytest.mark.parametrize("user", Valid_users)
    def test_compliant_data(self,sut: DAO,user: dict[str, Any]):
        result = sut.create(user)
        result.pop('_id')
        assert result == user