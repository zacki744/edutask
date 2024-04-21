import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO
import sys
import unittest.mock as mock
from unittest.mock import patch


@pytest.fixture(scope="module")
def sut():
    with patch('src.util.dao.getValidator', autospec=True) as mock_getValdator:
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "the first name of a user must be determined"
                    }, 
                    "lastName": {
                        "bsonType": "string",
                        "description": "the last name of a user must be determined"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "the email address of a user must be determined",
                        "uniqueItems": True
                    },
                    "tasks": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId"
                        }
                    }
                }
            }
        }
        mock_getValdator.return_value = validator
        name = 'user'
        dao = DAO(name)
        yield dao
        dao.drop()

@pytest.mark.integration
def test_create_noncompliant_data(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 309473,
        'tasks': '["email": 456645]'
    }

    with pytest.raises(WriteError) as e:
        sut.create(data)
    assert e.value.code == 121
    
@pytest.mark.integration
def test_create_user_no_first_name(sut):
    data = {
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    with pytest.raises(WriteError) as e:
        sut.create(data)
    assert e.value.code == 121
        
@pytest.mark.integration
def test_create_user_no_last_name(sut):
    data = {
        'firstName': 'John',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    with pytest.raises(WriteError) as e:
        sut.create(data)
    assert e.value.code == 121
        
@pytest.mark.integration
def test_create_user_no_email(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'tasks': []
    }

    with pytest.raises(WriteError) as e:
        sut.create(data)
    assert e.value.code == 121

@pytest.mark.integration
def test_create_user_compliant_data(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = sut.create(data)

    assert result == {'_id': result['_id'], 'firstName': 'John', 'lastName': 'Doe', 'email': 'johndoe@example.com', 'tasks': []}
    sut.delete(result['_id']['$oid'])


# CRUD tests below
@pytest.mark.integration
def test_update_user(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }
    result = sut.create(data)
    user_id = result['_id']['$oid']
    update_data = {
        '$set': {
            'firstName': 'Jane'
        }
    }

    sut.update(user_id, update_data)
    updated_user = sut.findOne(user_id)

    assert updated_user['firstName'] == 'Jane'
    sut.delete(user_id)


@pytest.mark.integration
def test_read_user(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = sut.create(data)
    user_id = result['_id']

    user = sut.findOne(user_id['$oid'])
    print(user)

    assert user == result
    sut.delete(user_id['$oid'])
    

@pytest.mark.integration   
def test_delete_user(sut):
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = sut.create(data)
    user_id = result['_id']

    result = sut.delete(user_id['$oid'])
    result1 = sut.findOne(user_id['$oid'])
    assert result1 is None