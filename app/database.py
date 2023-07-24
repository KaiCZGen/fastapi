from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_pwd}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

lsession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Dependencies for every requests
def get_db():
    db = lsession()
    try:
        yield db
    finally:
        db.close()

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# # Database Connection
# # Only start server if database is connected
# while True:
#     try:
#         # instantiate conn object
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres' ,password = 'test', cursor_factory=RealDictCursor)
#         # Execute sql commands
#         cursor = conn.cursor()
#         print("Database successfully connected!")
#         break
#     except Exception as error:
#         print("failed to connect to datebase")
#         print(error)
#         time.sleep(2)