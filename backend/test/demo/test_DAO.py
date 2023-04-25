import pytest
from bson import ObjectId
from pymongo.errors import WriteError
from src.util.dao import DAO
from unittest.mock import MagicMock
from mongomock import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import pymongo




@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient()
    yield client
    client.close()


def test_create_noncompliant_data(mongo_client):
    dao = DAO('user')
    data = {
        'title': 'Complete project',
        'description': 'Finish project before deadline',
        'startdate': datetime.utcnow(),
        'duedate': datetime.utcnow() + timedelta(days=7),
        'requires': [ObjectId('6150f0a26b29d7aa2c2b8657'), ObjectId('6150f0a26b29d7aa2c2b8658')],
        'categories': ['work', 'programming'],
        'todos': [ObjectId('6150f0a26b29d7aa2c2b8659'), ObjectId('6150f0a26b29d7aa2c2b865a')],
        'video': ObjectId('6150f0a26b29d7aa2c2b865b')
    }

    with pytest.raises(WriteError):
        print(dao.create(data))

def test_create_task_compliant_data(mongo_client):
    dao = DAO('task')
    data = {
        'title': 'Complete project',
        'description': 'Finish project before deadline',
        'startdate': datetime.utcnow(),
        'duedate': datetime.utcnow() + timedelta(days=7),
        'requires': [ObjectId('6150f0a26b29d7aa2c2b8657'), ObjectId('6150f0a26b29d7aa2c2b8658')],
        'categories': ['work', 'programming'],
        'todos': [ObjectId('6150f0a26b29d7aa2c2b8659'), ObjectId('6150f0a26b29d7aa2c2b865a')],
        'video': ObjectId('6150f0a26b29d7aa2c2b865b')
    }
    
    result = dao.create(data)

    expected_result = {
        '_id': result['_id'],
        'title': 'Complete project',
        'description': 'Finish project before deadline',
        'startdate': {'$date': result['startdate']['$date']},
        'duedate': {'$date': result['duedate']['$date']},
        'requires': [{'$oid': str(id)} for id in data['requires']],
        'categories': data['categories'],
        'todos': [{'$oid': str(id)} for id in data['todos']],
        'video': {'$oid': str(data['video'])}
    }
    assert result == expected_result



def test_create_todo_compliant_data(mongo_client):
    dao = DAO('todo')
    data = {
        'description': 'Buy groceries',
        'done': False
    }

    result = dao.create(data)

    assert result == {'_id': result['_id'], 'description': 'Buy groceries', 'done': False}

def test_create_user_compliant_data(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = dao.create(data)

    assert result == {'_id': result['_id'], 'firstName': 'John', 'lastName': 'Doe', 'email': 'johndoe@example.com', 'tasks': []}

def test_create_video_compliant_data(mongo_client):
    dao = DAO('video')
    data = {
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    }

    result = dao.create(data)

    assert result == {'_id': result['_id'], 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}


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


def test_update_user(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }
    result = dao.create(data)

    user_id = result['_id']['$oid']

    update_data = {
    '$set': {
        'firstName': 'Jane'
    }
}

    dao.update(user_id, update_data)
    updated_user = dao.findOne(user_id)

    assert updated_user['firstName'] == 'Jane'

def test_read_user(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = dao.create(data)
    user_id = result['_id']

    user = dao.findOne(user_id['$oid'])

    assert user['_id'] == user_id
    assert user['firstName'] == 'John'
    assert user['lastName'] == 'Doe'
    assert user['email'] == 'johndoe@example.com'
    assert user['tasks'] == []
    
    
def test_delete_user(mongo_client):
    dao = DAO('user')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@example.com',
        'tasks': []
    }

    result = dao.create(data)
    user_id = result['_id']

    result = dao.delete(user_id['$oid'])
    result1 = dao.findOne(user_id['$oid'])
    assert result1 is None
    assert result == 1


def test_clean(mongo_client):
    dao = DAO('task')
    dao1 = DAO('todo')
    dao2 = DAO('user')
    dao3 = DAO('video')
    
    try:
        for r in dao1.find():
            dao1.delete(r['_id']['$oid'])
        for r in dao2.find():
            dao2.delete(r['_id']['$oid'])
        for r in dao3.find():
            dao3.delete(r['_id']['$oid'])
        for r in dao.find():
            dao.delete(r['_id']['$oid'])
    except:
        pass