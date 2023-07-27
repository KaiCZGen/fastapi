######## Defines all fixtures

from fastapi.testclient import TestClient
from app.main_orm import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from alembic import command
from app.oauth2 import create_access_token
from app import models
import pytest

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_pwd}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABSE_URL)

testing_lsession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

###################### data base condifugration for testing

@pytest.fixture
def session():
    # w/ almenbic
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # w alembic
    #command.downgrade("base")
    #command.upgrade("head")

    db = testing_lsession()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Dependencies for every requests
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # overide dependencies for testing -> new database for testing
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def add_user(client):
    user_data = {"email":"example@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    created_user = res.json()
    created_user['password'] = user_data["password"]
    return created_user

@pytest.fixture
def add_user_2(client):
    user_data = {"email":"example1@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    created_user = res.json()
    created_user['password'] = user_data["password"]
    return created_user

@pytest.fixture
def token(add_user):
    return create_access_token({"user_id":add_user["id"]})

@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def create_test_posts(add_user, add_user_2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": add_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": add_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": add_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": add_user_2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
