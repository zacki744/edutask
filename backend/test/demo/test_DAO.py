import pytest
from bson import ObjectId
from pymongo.errors import WriteError
from src.util.dao import DAO

from unittest.mock import MagicMock
from mongomock import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient()
    yield client
    client.close()


class TestDAO():
    def setup_method(self):
        self.dao_Video = DAO('video')
        self.dao_Task = DAO('task')
        self.dao_User = DAO('user')
        self.dao_Todo = DAO('todo')


    @pytest.mark.demo
    def test_create_noncompliant_data(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 309473,
            'tasks': '["email": 456645]'
        }

        with pytest.raises(WriteError):
            self.dao_Video.create(data)
        
    @pytest.mark.demo
    def test_create_user_no_first_name(self, mongo_client):
        data = {
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        with pytest.raises(WriteError):
            self.dao_Video.create(data)
            
    @pytest.mark.demo
    def test_create_user_no_last_name(self, mongo_client):
        data = {
            'firstName': 'John',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        with pytest.raises(WriteError):
            self.dao_Video.create(data)
            
    @pytest.mark.demo
    def test_create_user_no_email(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'tasks': []
        }

        with pytest.raises(WriteError):
            self.dao_Video.create(data)

    @pytest.mark.demo
    def test_create_task_compliant_data(self, mongo_client):
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
        result = self.dao_Task.create(data)

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
        self.dao_Task.delete(result['_id']['$oid'])


    @pytest.mark.demo
    def test_create_todo_compliant_data(self, mongo_client):
        data = {
            'description': 'Buy groceries',
            'done': False
        }

        result = self.dao_Todo.create(data)

        assert result == {'_id': result['_id'], 'description': 'Buy groceries', 'done': False}
        self.dao_Todo.delete(result['_id']['$oid'])


    @pytest.mark.demo
    def test_create_user_compliant_data(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        result = self.dao_User.create(data)

        assert result == {'_id': result['_id'], 'firstName': 'John', 'lastName': 'Doe', 'email': 'johndoe@example.com', 'tasks': []}
        self.dao_User.delete(result['_id']['$oid'])


    @pytest.mark.demo
    def test_create_video_compliant_data(self, mongo_client):
        data = {
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }

        result = self.dao_Video.create(data)

        assert result == {'_id': result['_id'], 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        self.dao_Video.delete(result['_id']['$oid'])


    @pytest.mark.demo
    def test_create_no_connection(self, mongo_client):
        mongo_client.close()
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        # check for active connection before attempting to create object
        with pytest.raises(Exception):
            self.dao_User.db.command('ping')
            self.dao_User.create(data)


    @pytest.mark.demo
    def test_update_user(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }
        result = self.dao_User.create(data)
        user_id = result['_id']['$oid']
        update_data = {
            '$set': {
                'firstName': 'Jane'
            }
        }

        self.dao_User.update(user_id, update_data)
        updated_user = self.dao_User.findOne(user_id)

        assert updated_user['firstName'] == 'Jane'
        self.dao_User.delete(user_id)


    @pytest.mark.demo
    def test_read_user(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        result = self.dao_User.create(data)
        user_id = result['_id']

        user = self.dao_User.findOne(user_id['$oid'])

        assert user['_id'] == user_id
        assert user['firstName'] == 'John'
        assert user['lastName'] == 'Doe'
        assert user['email'] == 'johndoe@example.com'
        assert user['tasks'] == []
        self.dao_User.delete(user_id['$oid'])
        

    @pytest.mark.demo   
    def test_delete_user(self, mongo_client):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'tasks': []
        }

        result = self.dao_User.create(data)
        user_id = result['_id']

        result = self.dao_User.delete(user_id['$oid'])
        result1 = self.dao_User.findOne(user_id['$oid'])
        assert result1 is None
        assert result == 1