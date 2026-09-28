from dotenv import load_dotenv
import os

load_dotenv()

class ConfigurationError(Exception):
    pass

class Config:
    def __init__(self):
        self.user = os.getenv("DB_USER")
        if not self.user:
            raise ConfigurationError("DB_USER not set")
        self.password = os.getenv("DB_PASSWORD")
        if not self.password:
            raise ConfigurationError("DB_PASSWORD not set")
        self.host = os.getenv("DB_HOST")
        if not self.host:
            raise ConfigurationError("DB_HOST not set")
        self.port = os.getenv("DB_PORT")
        if not self.port:
            raise ConfigurationError("DB_PORT not set")
        self.name = os.getenv("DB_NAME")
        if not self.name:
            raise ConfigurationError("DB_NAME not set")
