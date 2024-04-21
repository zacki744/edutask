import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController


class TestUserController:

    @pytest.fixture
    def sut():
        mockDAO = MagicMock()
        mock = UserController(dao=mockDAO)
        return mock
    
    @pytest.fixture
    def email_data():
    invalid_emails = [
        ('@email.com',),
        ('jane.doeemail.com',),
        ('jane.doe@.com',),
        ('jane.doe@emailcom',),
        ('jane.doe@email.',),
        ('jane@doe@email.com',),
        ('',),
    ]
        vallid = [
            'john@hotmail.com',
            'vallid@gmail.com',
        ]
        return vallid, invalid_emails
    
    @pytest.mark.unit
    def test_get_user_by_email_vallid_email(self, sut, email):
        vallid, _ = email
        for mail in vallid:
            sut.dao.find.return_value = [mail]
            assert sut.get_user_by_email(mail) == mail
     
    # Test case for an invalid email
    @pytest.mark.parametrize('invalid_email', [
        pytest.param(email, id=f'invalid_email_{i}')
        for i, email in enumerate(email_data[1])
    ])
    def test_get_user_by_invalid_email(sut, invalid_email):
        email = invalid_email[0]
        # Assert that a ValueError is raised for an invalid email
        with pytest.raises(ValueError):
            sut.get_user_by_email(email)
            
