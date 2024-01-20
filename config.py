import os
from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    """
    Contains configurations for the application like db url, etc
    """

    DEBUG = os.getenv("DEBUG", "False") == "True"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
