import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.mark.unit
def test_get_user_by_email_valid_exists():
    """Test if get_user_by_email returns a valid user that exists in the database."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": "test@example.com", "name": "Test User"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # act
    result = user_controller.get_user_by_email(email)

    # assert
    assert user == result
    
@pytest.mark.unit
def test_get_user_by_email_valid_not_exists():
    """Test if get_user_by_email returns None when a valid user doesn't exist in the database."""
    # arrange
    dao_mock = mock.MagicMock()
    dao_mock.find.return_value = []
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # act
    with pytest.raises(Exception) as e:
        user_controller.get_user_by_email(email)
    print(e)
    assert str(e.value) == "list index out of range"

@pytest.mark.unit
def test_get_user_by_email_invalid():
    """Test if get_user_by_email raises ValueError when an invalid email is passed in."""
    # arrange
    dao_mock = mock.MagicMock()
    user_controller = UserController(dao=dao_mock)
    email = "invalid_email"

    # assert
    with pytest.raises(ValueError) as e:
        # act
        user_controller.get_user_by_email(email)
    assert str(e.value) == "Error: invalid email address"

@pytest.mark.unit
def test_get_user_by_email_multiple_users():
    """Test if get_user_by_email returns the first user when multiple users with the same email exist in the database."""
    # arrange
    dao_mock = mock.MagicMock()
    users = [{"email": "test@example.com", "name": "Test User 1"},
            {"email": "test@example.com", "name": "Test User 2"},
            {"email": "test@example,com", "name": "Test User 3"}]
    dao_mock.find.return_value = users
    user_controller = UserController(dao=dao_mock)

    # act
    result = user_controller.get_user_by_email(users[0]["email"])

    # assert
    assert result == users[0]

@pytest.mark.unit
def test_get_user_by_email_white_space_search():
    """Test if get_user_by_email returns Exception when white space is used in the search."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": "test@example.com", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)

    # act
    result = user_controller.get_user_by_email(user["email"])
    
    # assert
    assert user == result

@pytest.mark.unit
def test_get_user_by_email_white_space_creation():
    """Test if get_user_by_email returns Exception when white space is used in the search."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": " test@example.com ", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)

    # act
    result = user_controller.get_user_by_email(user["email"])
    
    # assert
    assert user == result

@pytest.mark.unit    
def test_get_user_by_email_number_serch():
    """Test if get_user_by_email returns TypeError when non string is used in the search."""
    # arrange
    dao_mock = mock.MagicMock()
    user ={"email": "test@example.com", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)
    email = 123

    # act
    with pytest.raises(TypeError) as e:
        user_controller.get_user_by_email(email)
    # assert
    assert str(e.value) == "expected string or bytes-like object"

@pytest.mark.unit
def test_get_user_by_email_no_mail():
    """Test if get_user_by_email returns ValueError when empty string is used in the search."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": "test@example.com", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)
    email = ""

    # act
    with pytest.raises(ValueError) as e:
        user_controller.get_user_by_email(email)
    # assert
    assert str(e.value) == "Error: invalid email address"

    
@pytest.mark.unit    
def test_get_user_by_email_database_exception():
    """Test if get_user_by_email raises an exception when an exception is raised in the database layer.""" 
    # arrange
    dao_mock = mock.MagicMock()
    dao_mock.find.side_effect = Exception()
    user_controller = UserController(dao=dao_mock)
    email = "test@example.com"

    # assert
    with pytest.raises(Exception) as e:
        # act
        user_controller.get_user_by_email(email)
    assert str(e.value) == ""

@pytest.mark.unit
def test_get_user_by_eamail_non_ASCII_charekters():
    """Test if get_user_by_email return a user with a non-ASCII character is in the email."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": "中国@æøå.com", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)
    
    # act
    result = user_controller.get_user_by_email(user["email"])
    
    # assert
    assert user == result

@pytest.mark.unit
def test_get_user_by_email_special_charecters_long():
    """Test if get_user_by_email returns user when special charekters is used in the search and creation."""
    # arrange
    dao_mock = mock.MagicMock()
    user = {"email": "!#$%&'*+-/=?^_`{|}~@*+-/=?^{|}~.com", "name": "Test User 1"}
    dao_mock.find.return_value = [user]
    user_controller = UserController(dao=dao_mock)

    # act
    result = user_controller.get_user_by_email(user["email"])
    
    # assert
    assert user == result