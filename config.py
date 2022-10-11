import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'config.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    UPLOADS_FOLDER = os.path.join(basedir, 'uploads')