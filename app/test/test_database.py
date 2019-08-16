import pytest
from app.main.service.member_service import *
from app.main import create_app, db


# fixture for creating the flask application
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test')
    testing_client = flask_app.test_client()
    app = flask_app.app_context()
    app.push()

    yield testing_client

    app.pop()


def test_add_new_member():
    # given a new member
    data = {"name": "sam", "card_no": "b12345", "email": "sam@test.com", "password_hash": "test_sam"}
    # when they are not in the database
    response = add_new_member(data)
    # then they are added to the database
    assert response['status'] is 'success'

