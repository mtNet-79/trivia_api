from os import environ, path
from dotenv import load_dotenv



basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

password = environ.get('PASSWORD')
database_name = 'trivia'
database_path = 'postgres://{}:{}@{}/{}'.format('postgres', password, 'localhost:5432', database_name)


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY')
    # STATIC_FOLDER = 'static'
    # TEMPLATES_FOLDER = 'templates'
    
    # Database
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS Secrets
    # AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    # AWS_KEY_ID = environ.get('AWS_KEY_ID')

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format('postgres', password, 'localhost:5432', 'trivia_test')
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False






