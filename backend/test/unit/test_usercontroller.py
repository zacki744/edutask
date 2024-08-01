import pytest
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController

class TestUserController:
    # Fixture for one user
    @pytest.fixture
    def sut_one_user(self):
        returnVal = {
            'firstName': 'John', 
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
        }
        dao = MagicMock()
        dao.find.return_value = [returnVal]
        return UserController(dao)

    #Fixture for multiple users
    @pytest.fixture
    def sut_multiple_users(self):
        returnVal = [
            {
                'firstName': 'John', 
                'lastName': 'Doe',
                'email': 'john123@example.com'
            },
            {
                'firstName': 'not Jhon', 
                'lastName': 'not Doe',
                'email': 'john123@example.com'
            }
        ]
        dao = MagicMock()
        dao.find.return_value = returnVal
        return UserController(dao)
    
    # Fixture for the system under test (SUT).
    @pytest.fixture
    def sut(self):
        dao = MagicMock()
        mockres = UserController(dao=dao)
        return mockres
    
    @pytest.fixture
    def sut_no_user(self):
        dao = MagicMock()
        dao.find.return_value = []
        return UserController(dao)

    @pytest.fixture
    def sut_exception(self):
        dao = MagicMock()
        dao.find.side_effect = Exception('Mocked exception')
        return UserController(dao)
    
    @pytest.mark.unit
    def test_get_user_by_email_valid_email(self, sut_one_user):
        email = 'john.doe@example.com'
        assert sut_one_user.get_user_by_email(email) == {'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@example.com'}
        
    @pytest.mark.unit
    def test_get_user_by_email_multiple(self, sut_multiple_users):
        email = 'john123@example.com'
        assert sut_multiple_users.get_user_by_email(email) == {'firstName': 'John', 'lastName': 'Doe', 'email': 'john123@example.com'}

    @pytest.mark.unit
    @pytest.mark.parametrize('invalid_email',
        [
            ('janedoeemail.com'),
            ('.com'),
            ('invallid'),
            ('jane.doeemail'),
            (''),
        ])
    def test_get_user_by_email_invalid(self, sut, invalid_email):
        with pytest.raises(ValueError), patch('src.controllers.usercontroller.re.fullmatch') as mock_re:
            mock_re.return_value = False
            sut.get_user_by_email(email = invalid_email)


    @pytest.mark.unit
    def test_get_user_by_email_no_user(self, sut_no_user):
        email = 'nonexistent@example.com'

        with pytest.raises(IndexError), patch('src.controllers.usercontroller.re.fullmatch') as mock_re:
            mock_re.return_value = True
            sut_no_user.get_user_by_email(email)
    
    @pytest.mark.unit
    def test_database_error(self, sut_exception):
        with pytest.raises(Exception):
            sut_exception.get_user_by_email('anything@anything.com') # This should raise an exception because of the mocked exception