import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

def test_get_user_by_email_valid_exists():
    """Test if get_user_by_email returns a valid user that exists in the database."""
    # arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = [{"email": "test@example.com", "name": "Test User"}]
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # act
    user = user_controller.get_user_by_email(email)

    # assert
    assert user == {"email": "test@example.com", "name": "Test User"}

def test_get_user_by_email_valid_not_exists():
    """Test if get_user_by_email returns None when a valid user doesn't exist in the database."""
    # arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = []
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # act
    user = user_controller.get_user_by_email(email)

    # assert
    assert user == None

def test_get_user_by_email_invalid():
    """Test if get_user_by_email raises ValueError when an invalid email is passed in."""
    # arrange
    dao_mock = MagicMock()
    user_controller = UserController(dao=dao_mock)
    email = "invalid_email"

    # assert
    with pytest.raises(ValueError):
        # act
        user_controller.get_user_by_email(email)

def test_get_user_by_email_multiple_users():
    """Test if get_user_by_email returns the first user when multiple users with the same email exist in the database."""
    # arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = [{"email": "test@example.com", "name": "Test User 1"},
                                  {"email": "test@example.com", "name": "Test User 2"}]
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # act
    user = user_controller.get_user_by_email(email)

    # assert
    assert user == {"email": "test@example.com", "name": "Test User 1"}
    dao_mock.find.assert_called_with({'email': email})

def test_get_user_by_email_database_exception():
    """Test if get_user_by_email raises an exception when an exception is raised in the database layer."""
    # arrange
    dao_mock = MagicMock()
    dao_mock.find.side_effect = Exception()
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # assert
    with pytest.raises(Exception):
        # act
        user_controller.get_user_by_email(email)
