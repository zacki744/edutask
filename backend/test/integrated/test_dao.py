import json
from typing import Any
from mongomock import MongoClient
import pymongo
import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO
import sys
import unittest.mock as mock
from unittest.mock import patch

class TestIntegrated:
    """
    Testcases for the dao create method
    """
    Valid_users = [
        {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "joe@bloggs.com",
            "tasks": [1,2]
        },
        {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@doe.com",
            "tasks": [1,2]
        }
    ]
    Invalid_uniqueItems = [
                {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "joe@bloggs.com",
            "tasks": [1,1]
        },
        {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@doe.com",
            "tasks": [1,1]
        }
    ]
    Invalid_users_partials = [
        {
            "lastName": "Bloggs",
            "email": "joe@bloggs.com",
            "tasks": []
        },
        {
            "firstName": "Joe",
            "email": "joe@bloggs.com",
            "tasks": []
        },
                {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "tasks": []
        },
        {},
    ]
    Invalid_Data_Types = [
        {
            "firstName": True,
            "lastName": "Bloggs",
            "email": "joe@bloggs.com",
            "tasks": []
        },
        {
            "firstName": "Joe",
            "lastName": [],
            "email": "joe@bloggs.com",
            "tasks": []
        },
        {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": 123,
            "tasks": []
        },
        {
            "firstName": False,
            "lastName": False,
            "email": False
        }
    ]
    @pytest.fixture(scope="module")
    def sut(self):
        """System Under Test (SUT).

        Yields:
            DAO:  mocked getValidation
        """
        with open ('./test.json', 'r') as f:
            validator = json.load(f)
        with patch('src.util.dao.getValidator', autospec=True) as mock_getValdator:
            mock_getValdator.return_value = validator
            sut = DAO("test")
        client = MongoClient('localhost', 27017)
        db = client['edutask']
        yield sut
        sut.collection.drop()

    @pytest.mark.dao
    @pytest.mark.parametrize("user", Invalid_Data_Types)
    def test_Invalid_Data_Types(self, sut: DAO, user: Any):
        with pytest.raises(WriteError):
            sut.create(user)
    
    @pytest.mark.dao
    @pytest.mark.parametrize("user", Invalid_users_partials)
    def test_Invalid_users_partials(self, sut: DAO, user: Any):
        with pytest.raises(WriteError):
            sut.create(user)

    @pytest.mark.dao
    @pytest.mark.parametrize("user", Invalid_uniqueItems)
    def test_Invalid_uniqueItems(self, sut: DAO, user: dict[str, Any]):
        with pytest.raises(WriteError):
            sut.create(user)
    
    @pytest.mark.dao
    @pytest.mark.parametrize("user", Valid_users)
    def test_complient_data(self,sut: DAO,user: dict[str, Any]):
        result = sut.create(user)
        result.pop('_id')
        assert result == user