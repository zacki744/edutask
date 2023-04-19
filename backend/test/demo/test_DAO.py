import pytest
from bson import json_util
from pymongo.errors import WriteError
from src.util.dao import DAO
from unittest.mock import MagicMock
from mongomock import MongoClient
import pymongo


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient()
    yield client
    client.close()

def test_create_compliant_data(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = dao.create(data)

    assert result == {'_id': result['_id'], 'firstName': 'John', 'lastName': 'Doe', 'email': 'johndoe@example.com', 'tasks': []}

def test_create_noncompliant_data(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John'
    }

    with pytest.raises(pymongo.errors.OperationFailure):
        print(dao.create(data))



def test_create_no_connection(mongo_client):
    mongo_client.close()
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    # check for active connection before attempting to create object
    with pytest.raises(Exception):
        dao.db.command('ping')
        dao.create(data)
