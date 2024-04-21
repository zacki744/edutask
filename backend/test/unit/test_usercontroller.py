import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController


class TestUserController:

    @pytest.fixture
    def sut(self):
        mockDAO = MagicMock()
        mock = UserController(dao=mockDAO)
        return mock
    
    @pytest.fixture
    def email(self):
        invallid = [
            'invalid',  # missing '@' symbol
            'invalid.email.com',
        ]
        vallid = [
            'john@hotmail.com',
            'vallid@gmail.com',
        ]
        return vallid, invallid
    
    @pytest.mark.unit
    def test_get_user_by_email_vallid_email(self, sut, email):
        vallid, _ = email
        for mail in vallid:
            sut.dao.find.return_value = [mail]
            assert sut.get_user_by_email(mail) == mail
     
    @pytest.mark.unit
    def test_get_user_by_email_invallid_email(self, sut, email):
        _, invallid = email
        for mail in invallid:
            print(mail)
            with pytest.raises(ValueError):
                sut.get_user_by_email(mail)
        
