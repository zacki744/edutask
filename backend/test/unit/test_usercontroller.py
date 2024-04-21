import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

class TestUserController:

    # Fixture for creating a UserController instance with a mocked DAO
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
                'firstName': 'John', 
                'lastName': 'Doe',
                'email': 'john123@example.com'
            }
        ]
        dao = MagicMock()
        dao.find.return_value = returnVal
        return UserController(dao)

    @pytest.fixture
    def sut(self):
        dao = MagicMock()
        mockres = UserController(dao=dao)
        return mockres

    # Test case for a valid email
    @pytest.mark.unit
    def test_validate_email_valid_email(self, sut_one_user):
        email = 'john.doe@example.com'
        
        assert sut_one_user.get_user_by_email(email) == {'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@example.com'}
        
    # Test case for an multiple user with same email, shuld return only one user
    @pytest.mark.unit
    def test_email_multiple(self, sut_multiple_users):
        email = 'john123@example.com'
        assert sut_multiple_users.get_user_by_email(email) == {'firstName': 'John', 'lastName': 'Doe', 'email': 'john123@example.com'}

    # Test case for an invalid email
    invalid_email_1 = 'jane.doeemail.com'
    invalid_email_2 = '.com'
    invalid_email_3 = 'this_is_not_an_email'
    invalid_email_4 = 'jane.doeemail'
    invalid_email_5 = ''

    @pytest.mark.unit
    @pytest.mark.parametrize('invalid_email',
                            [
                                (invalid_email_1),
                                (invalid_email_2),
                                (invalid_email_3),
                                (invalid_email_4),
                                (invalid_email_5),
                            ])
    def test_get_user_by_email_invalid(self, sut, invalid_email):
            with pytest.raises(ValueError):
                sut.get_user_by_email(email = invalid_email)