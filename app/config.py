from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# create env variables
class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_pwd : str
    database_name : str
    database_username : str
    token_pwd : str #using key like secrect_key cause error
    algorithm : str
    access_token_expire : int

    class Config:
        env_file = ".env"
        extra="allow"

settings = Settings()