"""
Flask configuration variables.
"""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration from .env file."""
    # General Config
    #SECRET_KEY = 'honey'
    SECRET_KEY = 'lydia'
    FLASK_APP = 'forum.app'
    #engine = create_engine("mysql+mysqldb://chrism:lesson@localhost/data5zero")
    # Database
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///circuscircus.db'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chrism:lesson@localhost/circuscircus'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chrism:lesson@localhost/circuscircus' #
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:deep7573_mysql@localhost/circuscircus' # 'sqlite:///circuscircus.db'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lydia:celeste@localhost/circuscircus'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False