from fastapi.testclient import TestClient
from app.main_orm import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from alembic import command
import pytest

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_pwd}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABSE_URL)

testing_lsession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

###################### data base condifugration for testing

@pytest.fixture()
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

@pytest.fixture()
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